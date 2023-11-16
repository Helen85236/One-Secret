db = db.getSiblingDB('admin');

db.auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);

db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

db.createUser({
    user: '1'+process.env.MONGO_INITDB_ROOT_USERNAME,
    pwd:  '1'+process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [
      {
        role: 'root',
        db: process.env.MONGO_INITDB_DATABASE,
      },
    ],
  });
