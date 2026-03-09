---
title: "Solving Event Losses with Kafka Dead Letter Queue"
url: https://medium.com/p/d47538b27697
---

# Solving Event Losses with Kafka Dead Letter Queue

[Original](https://medium.com/p/d47538b27697)

# Solving Event Losses with Kafka Dead Letter Queue

[![Orçun Yılmaz](https://miro.medium.com/v2/resize:fill:64:64/1*R7PoDxDMl36A3lSLTxEHkQ@2x.jpeg)](/@orcunyilmazoy?source=post_page---byline--d47538b27697---------------------------------------)

[Orçun Yılmaz](/@orcunyilmazoy?source=post_page---byline--d47538b27697---------------------------------------)

8 min read

·

Aug 1, 2023

--

1

Listen

Share

More

![]()

Kafka is a distributed streaming platform that excels in processing millions of messages per second while maintaining high availability and fault tolerance. However, in real-world scenarios, certain challenges, such as network-related issues, can lead to event losses. In this article, we will explore the implementation of **Kafka Dead Letter Queue (DLQ)** to address event loss problems. We will use an example of an **Order Service** application that generates Kafka events and demonstrate how to write these events into a database table. This comprehensive guide will cover both the producer and consumer sides of the implementation in Java.

## The Problem of Event Losses

Kafka’s reliability heavily relies on stable network connectivity between clients and brokers. Unfortunately, some situations even in your network or in your code can lead to event losses, even with default configurations that are typically conservative enough to avoid such issues.

In a nutshell, **Event Loss** means that certain events that were expected to be processed or consumed are not received or processed by the intended recipients, resulting in data inconsistency and potential issues within the system.

And those issues are not going to be small ones, based on the scenario you have. Some of them may be even on a catastrophic scale.

## Outbox Pattern to Prevent Event Losses

To prevent event losses caused by network-related problems, the **Outbox Pattern** can be employed.

The **Outbox Pattern** aims to prevent event loss and ensure data consistency when producing and consuming events in distributed systems like Kafka. It accomplishes this by decoupling the act of producing events from the main business transaction. Instead of immediately publishing events to the message broker within the same transaction, the pattern introduces an intermediate storage layer known as the “**outbox**.”

In this pattern, instead of directly sending events to Kafka, a document containing event details (key, value, headers, topic) is added to a storage system, such as **MongoDB,** or some another Kafka topic, using the **Kafka Error Handler API**. Later, these events are sent to the specified topic using a Kafka source connector, effectively preventing event loss in case of any errors.

## How the Outbox Pattern Works:

1. **Producing Events to the Outbox**: When an event is generated as part of a business transaction, instead of immediately sending it to the message broker, the event is first stored in the outbox. The outbox acts as a persistent and reliable storage mechanism for events.
2. **Main Transaction Completes**: Once the main business transaction successfully completes, including any necessary database updates or state changes, the outbox is also committed as part of the same transaction.
3. **Asynchronous Publishing**: After the transaction commits successfully, a separate process asynchronously reads the events from the outbox and publishes them to the message broker. This asynchronous publishing ensures that event delivery does not block the main transaction, reducing the risk of event loss due to network-related issues.

## DLQ Comes Into Play

Let’s say we have an Order Service, which handles the order events. We are going to implement DLQ into this service.

**Producer** code below:

```
public class OrderProducer {  
  
    private KafkaTemplate<String, String> kafkaTemplate;  
    private String orderTopic;  
    private String orderDlqTopic;  
  
    public OrderProducer(KafkaTemplate<String, String> kafkaTemplate, String orderTopic, String orderDlqTopic) {  
        this.kafkaTemplate = kafkaTemplate;  
        this.orderTopic = orderTopic;  
        this.orderDlqTopic = orderDlqTopic;  
    }  
  
    public void sendOrder(Order order) {  
        String orderJson = convertOrderToJson(order);  
        ProducerRecord<String, String> producerRecord = new ProducerRecord<>(orderTopic, order.getId(), orderJson);  
  
        kafkaTemplate.send(producerRecord)  
                .addCallback(  
                        result -> handleSendSuccess(result, order),  
                        ex -> handleSendError(ex, producerRecord)  
                );  
    }  
  
    private void handleSendSuccess(SendResult<String, String> result, Order order) {  
        // Assuming further processing and logic after successful sending  
    }  
  
    private void handleSendError(Throwable ex, ProducerRecord<String, String> producerRecord) {  
        // Handle the failed message by sending it to the DLQ  
        kafkaTemplate.send(orderDlqTopic, producerRecord.key(), producerRecord.value());  
    }  
  
    private String convertOrderToJson(Order order) {  
        // Convert Order object to JSON string  
        return ""; // JSON representation of the order  
    }  
}
```

The provided `OrderProducer` class demonstrates how to produce messages to a Kafka topic using the Spring Kafka `KafkaTemplate`. It implements basic error handling by sending failed messages to a Dead Letter Queue (DLQ). You may either define another topic for your failed messages, or you may consider writing them into a database table.

You should be aware of the situation that, if you are willing to write failed messages into a table, or somewhere like Redis, you should also have a batch process to collect them, then fire them again with a re-try mechanism.

**Consumer** code below:

```
public class OrderConsumer {  
  
    private KafkaTemplate<String, String> kafkaTemplate;  
    private String orderDlqTopic;  
  
    public OrderConsumer(KafkaTemplate<String, String> kafkaTemplate, String orderDlqTopic) {  
        this.kafkaTemplate = kafkaTemplate;  
        this.orderDlqTopic = orderDlqTopic;  
    }  
  
    @KafkaListener(topics = "${order.topic}")  
    public void processOrder(ConsumerRecord<String, String> record) {  
        String orderId = record.key();  
        String orderJson = record.value();  
  
        // Convert JSON to Order object  
        Order order = convertJsonToOrder(orderJson);  
  
        try {  
            // Process the order  
            processOrderLogic(order);  
  
            // Assuming further processing and logic after consuming the order  
        } catch (Exception e) {  
            // Handle the exception by sending the failed message to the DLQ  
            sendToDlq(orderId, orderJson);  
        }  
    }  
  
    private void processOrderLogic(Order order) {  
        // Process the order based on domain-specific logic  
    }  
  
    private Order convertJsonToOrder(String orderJson) {  
        // Convert JSON string to Order object  
        return new Order(); // Placeholder for JSON conversion logic  
    }  
  
    private void sendToDlq(String orderId, String orderJson) {  
        kafkaTemplate.send(orderDlqTopic, orderId, orderJson);  
    }  
}
```

The provided `OrderConsumer` class demonstrates how to consume messages from a Kafka topic using the Spring Kafka framework. It includes a Kafka listener method (`processOrder`) that listens to messages from the specified topic and processes them based on domain-specific logic. If an exception occurs during message processing, the failed message is sent to the Dead Letter Queue (DLQ) topic using the `kafkaTemplate`.

Again, you may consider writing failed reads into a database table or Redis kind of storage with a batch process that collects and fires them again with a re-try logic.

## Pros of using Kafka Dead Letter Queue (DLQ)

**Error Handling**: DLQ allows you to handle and store messages that couldn’t be successfully processed by the consumers. This helps in identifying and analyzing problematic messages, enabling you to take corrective actions.

**Message Retention**: DLQ ensures that failed messages are retained in a separate topic for a specified duration, even if they couldn’t be successfully processed. This retention period allows developers and operators to investigate and replay failed messages for debugging and recovery purposes.

**Separation of Concerns**: By using a DLQ, you separate the failed messages from the main topic, which helps maintain the integrity and performance of the main topic.

**Automatic Retry**: In some cases, failed messages in the DLQ can be automatically retried for processing, reducing the need for manual intervention.

**Scalability**: DLQs allow you to scale the consumer processing independently of the failed message handling, ensuring that failed messages are dealt with efficiently.

**Error Tracking and Monitoring**: DLQs can be closely monitored to track error rates and patterns, allowing teams to identify and resolve systemic issues.

## Cons of using Kafka Dead Letter Queue (DLQ)

**Message Duplication**: When messages are sent to the DLQ, it may lead to duplication of data, as the same message is present in both the main topic and the DLQ. This duplication requires additional handling and deduplication logic.

**Storage Overhead**: Storing failed messages in a separate DLQ topic can result in additional storage overhead, especially if the failure rate is high or if the retention period is long.

**Operational Complexity**: Introducing a DLQ adds an extra level of complexity to the system. It requires careful configuration, monitoring, and maintenance to ensure proper handling of failed messages.

**Potential Retries**: If not configured carefully, failed messages in the DLQ may be retried indefinitely, potentially leading to excessive resource usage and performance issues.

**Message Order**: Depending on the DLQ configuration and consumer implementation, the order of processing may not be guaranteed. Failed messages may be processed out of order, affecting the consistency of the system.

**Delayed Error Detection**: In some cases, failed messages may not immediately appear in the DLQ, causing a delay in detecting errors and failures in the system.

## Message Duplication is Crucial

Message duplication in a Dead Letter Queue (DLQ) can occur if the DLQ topic is not properly managed and configured, and it is one of the most common problems that you may come across when you start experiencing DLQ. There are a few scenarios where message duplication can happen in a DLQ:

**Incorrect Message Acknowledgment**: If the consumer processing the messages from the main topic and sending them to the DLQ does not handle acknowledgments correctly, it may lead to duplicate messages being sent to the DLQ. For example, if the acknowledgment is not sent after processing the message from the main topic, the consumer may retry sending the message to the DLQ, resulting in duplication.

**Consumer Retry Logic**: In some cases, the consumer that processes messages from the main topic may have its own retry logic. If this retry logic is not coordinated with the DLQ handling, it may lead to duplicate messages being sent to the DLQ.

**Redelivery of DLQ Messages**: If the configuration of the DLQ topic allows for message redelivery after a certain period of time, and the consumer that processes messages from the DLQ does not have proper deduplication logic, it may lead to messages being processed multiple times.

**Improper DLQ Configuration**: If the DLQ topic is not configured properly, it may not enforce proper message deduplication or may allow for messages to be sent to the DLQ multiple times.

**Network or Infrastructure Issues**: In rare cases, network or infrastructure issues can cause messages to be duplicated, including messages sent to the DLQ.

To prevent message duplication in the DLQ, it is essential to follow best practices and ensure proper configuration and coordination between the main topic and the DLQ handling. Some steps to avoid message duplication in the DLQ include:

**Use Idempotent Producers**: Ensure that the producer sending messages to the DLQ is idempotent, meaning it can handle duplicate messages without causing side effects.

**Proper Acknowledgment**: Make sure that the acknowledgment mechanism is correctly implemented to avoid sending duplicate messages to the DLQ.

**Deduplication Logic**: Implement proper deduplication logic in both producers and consumers that processes messages from the DLQ to prevent processing the same message multiple times.

**Configure DLQ Retention**: Set an appropriate retention period for messages in the DLQ to avoid unnecessary redelivery of old messages.

**Monitor and Alert**: Regularly monitor the DLQ for any unusual activity or message duplication and set up alerts to notify the operations team in case of issues.

By following these practices and ensuring proper configuration and coordination, you can minimize the chances of message duplication in the DLQ and ensure the effective handling of failed messages in the system.

In conclusion, using a Dead Letter Queue (DLQ) in Kafka can significantly improve error handling, monitoring, and resilience in the system. However, it also introduces some complexities and considerations that need to be carefully managed to avoid potential issues like message duplication, storage overhead, and operational challenges. Proper configuration and monitoring are essential to ensure the effective and efficient use of Kafka DLQ.