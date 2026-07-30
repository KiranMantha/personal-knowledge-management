---
type: Learning
title: setup mongodb locally
topic: Backend_Databases_etc
tags:
  - mongodb
  - setup
status: stable
generated:
  by: 'human:kiran'
  at: '2026-07-30T07:06:38.811Z'
verified:
  - by: agent-kiran/seed-script
    at: '2026-07-30T07:06:38.811Z'
---
# Install mongodb

## With homebrew

- https://medium.com/create-a-clocking-in-system-on-react/creating-a-local-mongodb-database-and-insert-a-document-c6a4a2102a22

- run below commands:

```bash
brew tap mongodb/brew
```

```bash
brew install mongodb-community
```

- after installation, to start mongodb, run `brew services start mongodb-community`.
- to check this: install mongodb vscode extension and add a connection with connection string: `mongodb://localhost`.
- to stop mongodb, run `brew services stop mongodb-community`.

## With docker

- install docker and start it
- run `docker run --name mymongodb -d -p 27017:27017 mongo`
- this will pull the latest `mongo` image and run a container named `mymongodb` on external port 27017 and internal port 27017 in detached and published mode
- to start using local mongodb, install mongodb vscode extension and add a connection with connection string: `mongodb://localhost:27017`.

### Pro-tips

- To backup database
```bash
mongodump --host=localhost --gzip --db <your-database-name> --archive=/<your-backup-folder-location>/<backup-file-name>.gz
```

- To restore database from backup

```bash
mongorestore --gzip --archive=/<your-backup-folder-location>/<backup-file-name>.gz
```

- To backup all databases

```bash
mongodump --out /<your-backup-folder-location>
```

### Useful links

https://www.geeksforgeeks.org/how-to-back-up-and-restore-a-mongodb-database/
