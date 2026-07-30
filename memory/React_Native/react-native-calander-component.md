---
type: Learning
title: React-Native calander component
topic: React_Native
tags:
  - react-native
  - ui
status: stable
generated:
  by: 'human:kiran'
  at: '2026-07-30T07:06:31.646Z'
verified:
  - by: agent-kiran/seed-script
    at: '2026-07-30T07:06:31.646Z'
---
```tsx
// Calander.tsx
import i18n from '@/i18n';
import { FontAwesome } from '@expo/vector-icons';
import { ReactNode, useEffect, useState } from 'react';
import { FlatList, Modal, Pressable, Text, TouchableOpacity, View } from 'react-native';
import { getStyles } from './Calander.styles';

type CalendarModalProps = {
  initialDate?: string;
  yearRange?: { start: number; end: number };
  disablePastDates?: boolean;
  children: ReactNode;
  onDateSelection: (date: string) => void;
};

const normalize = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
const isBeforeToday = (date: Date) => normalize(date) < normalize(new Date());
const parseDate = (str: string): Date => new Date(str);
const formatDate = (date: Date): string => {
  const year = date.getFullYear();
  const month = `${date.getMonth() + 1}`.padStart(2, '0');
  const day = `${date.getDate()}`.padStart(2, '0');
  return `${year}-${month}-${day}`; // ✅ Local-safe formatting
};

export const Calendar = ({
  initialDate,
  disablePastDates = true,
  yearRange,
  children,
  onDateSelection
}: CalendarModalProps) => {
  const locale = i18n.language;
  const isRTL = locale === 'ar';
  const styles = getStyles();
  const today = new Date();
  const selectedDate = initialDate ? parseDate(initialDate) : today;
  const [modalVisible, setModalVisible] = useState(false);
  const [currentMonth, setCurrentMonth] = useState(selectedDate.getMonth());
  const [currentYear, setCurrentYear] = useState(selectedDate.getFullYear());
  const [highlightedDate, setHighlightedDate] = useState(selectedDate);
  const [yearPickerVisible, setYearPickerVisible] = useState(false);
  const [monthPickerVisible, setMonthPickerVisible] = useState(false);

  const getLocalizedDays = () => {
    const baseDate = new Date(2023, 0, 1); // Jan 1st, 2023 is a Sunday
    return Array.from({ length: 7 }).map((_, i) =>
      new Date(baseDate.getTime() + i * 86400000).toLocaleDateString(locale, {
        weekday: 'short'
      })
    );
  };

  const getDaysInMonth = (month: number, year: number): (Date | null)[] => {
    const days: (Date | null)[] = [];
    const firstDay = new Date(year, month, 1).getDay(); // Sunday = 0
    const totalDays = new Date(year, month + 1, 0).getDate();

    // Leading empty cells
    for (let i = 0; i < firstDay; i++) {
      days.push(null);
    }

    // Actual days
    for (let i = 1; i <= totalDays; i++) {
      days.push(new Date(year, month, i));
    }

    // Trailing empty cells
    const totalCells = days.length;
    const remainder = totalCells % 7;
    if (remainder !== 0) {
      const trailingEmptyCells = 7 - remainder;
      for (let i = 0; i < trailingEmptyCells; i++) {
        days.push(null);
      }
    }

    return days;
  };

  const changeMonth = (increment: number) => {
    let newMonth = currentMonth + increment;
    let newYear = currentYear;

    if (newMonth > 11) {
      newMonth = 0;
      newYear++;
    } else if (newMonth < 0) {
      newMonth = 11;
      newYear--;
    }

    // ❌ Block if out of yearRange
    if (yearRange) {
      if (newYear < yearRange.start || newYear > yearRange.end) return;
    }

    // ✅ Block going to past months if disablePastDates is set
    if (disablePastDates) {
      const targetDate = new Date(newYear, newMonth, 1);
      const startOfToday = new Date(today.getFullYear(), today.getMonth(), 1);
      if (targetDate < startOfToday) return;
    }

    setCurrentMonth(newMonth);
    setCurrentYear(newYear);
  };

  const isSameMonth = (date: Date) => date.getMonth() === currentMonth && date.getFullYear() === currentYear;

  const isHighlighted = (date: Date): boolean =>
    highlightedDate &&
    date.getDate() === highlightedDate.getDate() &&
    date.getMonth() === highlightedDate.getMonth() &&
    date.getFullYear() === highlightedDate.getFullYear();

  const getYears = () => {
    const now = new Date();
    const min = yearRange?.start ?? now.getFullYear() - 50;
    const max = yearRange?.end ?? now.getFullYear() + 50;
    return Array.from({ length: max - min + 1 }, (_, i) => min + i);
  };

  const getMonths = () => {
    return Array.from({ length: 12 }, (_, i) => new Date(2000, i, 1).toLocaleDateString(locale, { month: 'short' }));
  };

  const renderDay = ({ item }: { item: Date | null }) => {
    if (!item) return <View style={styles.dayCell} />;

    const isOutOfMonth = !isSameMonth(item);
    const isPast = disablePastDates && isBeforeToday(item);
    const isDisabled = isOutOfMonth || isPast;

    return (
      <TouchableOpacity
        style={[styles.dayCell, isHighlighted(item) && styles.highlighted, isDisabled && styles.disabled]}
        disabled={isDisabled}
        onPress={() => {
          setHighlightedDate(item);
          onDateSelection(formatDate(item));
          setModalVisible(false);
        }}
      >
        <Text
          style={[styles.dayText, isHighlighted(item) && styles.highlightedText, isDisabled && styles.disabledText]}
        >
          {item.getDate()}
        </Text>
      </TouchableOpacity>
    );
  };

  const localizedDays = getLocalizedDays();
  const days = getDaysInMonth(currentMonth, currentYear);
  const months = getMonths();
  const years = getYears();

  useEffect(() => {
    if (modalVisible) {
      const base = initialDate ? parseDate(initialDate) : today;
      setCurrentMonth(base.getMonth());
      setCurrentYear(base.getFullYear());
      setHighlightedDate(base);
      setMonthPickerVisible(false);
      setYearPickerVisible(false);
    }
  }, [modalVisible]);

  return (
    <>
      <TouchableOpacity
        onPress={() => {
          setModalVisible(true);
        }}
      >
        {children}
      </TouchableOpacity>
      <Modal transparent visible={modalVisible} animationType="slide">
        <Pressable
          style={styles.modalOverlay}
          onPress={() => {
            if (yearPickerVisible) setYearPickerVisible(false);
            else if (monthPickerVisible) setMonthPickerVisible(false);
            else setModalVisible(false);
          }}
        >
          <Pressable onPress={() => {}} style={styles.modalContent}>
            <View style={styles.header}>
              <TouchableOpacity
                disabled={
                  disablePastDates &&
                  new Date(currentYear, currentMonth - 1, 1) < new Date(today.getFullYear(), today.getMonth(), 1)
                }
                onPress={() => changeMonth(isRTL ? 1 : -1)}
              >
                <FontAwesome
                  name="chevron-left"
                  style={[
                    styles.nav,
                    disablePastDates &&
                      new Date(currentYear, currentMonth - 1, 1) <
                        new Date(today.getFullYear(), today.getMonth(), 1) && {
                        color: '#ccc'
                      }
                  ]}
                />
              </TouchableOpacity>

              <View style={{ flexDirection: 'row', gap: 10 }}>
                <TouchableOpacity
                  onPress={() => {
                    setMonthPickerVisible((v) => !v);
                    if (!monthPickerVisible) {
                      setYearPickerVisible(false);
                    }
                  }}
                >
                  <Text style={styles.title}>{months[currentMonth]}</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  onPress={() => {
                    setYearPickerVisible((v) => !v);
                    if (!yearPickerVisible) {
                      setMonthPickerVisible(false);
                    }
                  }}
                >
                  <Text style={styles.title}>{currentYear}</Text>
                </TouchableOpacity>
              </View>

              <TouchableOpacity onPress={() => changeMonth(isRTL ? -1 : 1)}>
                <FontAwesome name="chevron-right" style={styles.nav} />
              </TouchableOpacity>
            </View>

            {monthPickerVisible && (
              <View style={styles.pillGrid}>
                {months.map((m, i) => {
                  const isDisabled = disablePastDates && currentYear === today.getFullYear() && i < today.getMonth();

                  return (
                    <TouchableOpacity
                      key={m}
                      style={[styles.pill, i === currentMonth && styles.pillSelected, isDisabled && styles.disabled]}
                      disabled={isDisabled}
                      onPress={() => {
                        setCurrentMonth(i);
                        setMonthPickerVisible(false);
                      }}
                    >
                      <Text
                        style={[
                          styles.pillText,
                          i === currentMonth && styles.pillTextSelected,
                          isDisabled && styles.disabledText
                        ]}
                      >
                        {m}
                      </Text>
                    </TouchableOpacity>
                  );
                })}
              </View>
            )}

            {yearPickerVisible && (
              <View style={styles.pillGrid}>
                {years.map((year) => (
                  <TouchableOpacity
                    key={year}
                    style={[styles.pill, year === currentYear && styles.pillSelected]}
                    onPress={() => {
                      setCurrentYear(year);
                      setYearPickerVisible(false);
                    }}
                  >
                    <Text style={[styles.pillText, year === currentYear && styles.pillTextSelected]}>{year}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            )}

            <View style={[styles.daysRow, isRTL && { flexDirection: 'row-reverse' }]}>
              {localizedDays.map((day) => (
                <Text key={day} style={styles.dayLabel}>
                  {day}
                </Text>
              ))}
            </View>

            <FlatList
              data={days}
              renderItem={renderDay}
              keyExtractor={(item, index) => item?.toISOString() || `empty-${index}`}
              numColumns={7}
              scrollEnabled={false}
            />

            <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeBtn}>
              <Text style={styles.closeText}>Cancel</Text>
            </TouchableOpacity>
          </Pressable>
        </Pressable>
      </Modal>
    </>
  );
};
```

```tsx
//Calander.styles.ts
import { StyleSheet } from 'react-native';

export const getStyles = () => {
  return StyleSheet.create({
    modalOverlay: {
      flex: 1,
      justifyContent: 'center',
      backgroundColor: '#00000088',
      padding: 20
    },
    modalContent: {
      backgroundColor: 'white',
      borderRadius: 8,
      padding: 16,
      elevation: 5
    },
    header: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: 10,
      paddingHorizontal: 14
    },
    nav: {
      fontSize: 20,
      fontWeight: 'bold'
    },
    title: {
      fontSize: 16,
      fontWeight: 'bold',
      textAlign: 'center'
    },
    daysRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      marginVertical: 6
    },
    dayLabel: {
      flex: 1,
      textAlign: 'center',
      fontWeight: '600'
    },
    dayCell: {
      flex: 1,
      height: 40,
      margin: 2,
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: 4
    },
    highlighted: {
      backgroundColor: '#0045ff'
    },
    dayText: {
      color: '#333'
    },
    disabled: {
      backgroundColor: '#eee'
    },
    highlightedText: {
      color: '#fff'
    },
    disabledText: {
      color: '#aaa'
    },
    closeBtn: {
      marginTop: 10,
      padding: 8,
      alignSelf: 'center'
    },
    closeText: {
      color: '#0045ff',
      fontWeight: 'bold'
    },
    pillGrid: {
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'center',
      marginBottom: 10
    },
    pill: {
      paddingHorizontal: 12,
      paddingVertical: 6,
      margin: 4,
      borderRadius: 20,
      borderWidth: 1,
      borderColor: '#ccc'
    },
    pillSelected: {
      backgroundColor: '#0045ff',
      borderColor: '#0045ff'
    },
    pillText: {
      fontSize: 14,
      color: '#333'
    },
    pillTextSelected: {
      color: '#fff'
    }
  });
};
```
