---
title: "GraphQL Subscriptions in NestJS with Apache Kafka, and MongoDB"
url: https://medium.com/p/86ee0a64a116
---

# GraphQL Subscriptions in NestJS with Apache Kafka, and MongoDB

[Original](https://medium.com/p/86ee0a64a116)

# GraphQL Subscriptions in NestJS with Apache Kafka, and MongoDB

[![Sahan Kodituwakku](https://miro.medium.com/v2/resize:fill:64:64/1*pS2uRD_IF3deWZjK50Ikow.jpeg)](https://medium.com/@sahan.kodituwakku?source=post_page---byline--86ee0a64a116---------------------------------------)

[Sahan Kodituwakku](https://medium.com/@sahan.kodituwakku?source=post_page---byline--86ee0a64a116---------------------------------------)

11 min read

·

Mar 12, 2024

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

Let’s see how to implement GraphQL subscription feature inside a NestJS application backed with a Apache Kafka Publish/Subscribe, a MongoDB database and a Apollo GraphQL Server.

> GraphQL subscriptions are a way to push data from the server to the clients that choose to listen to real time messages from the server. Subscriptions are similar to queries in that they specify a set of fields to be delivered to the client, but instead of immediately returning a single answer, a channel is opened and a result is sent to the client every time a particular event happens on the server.
>
> adapted from [GraphQL + TypeScript — Subscriptions | NestJS — A progressive Node.js framework](https://docs.nestjs.com/graphql/subscriptions)

**Note:** Production apps should use a PubSub implementation backed by an external store. In this case, we use Apache Kafka with Kafkajs.

First let’s install the Nest CLI and then crate a new NestJS project. I am using pnpm as the package manager for this project.

```
npm i -g @nestjs/cli  
nest new graphql-pubsub-kafka
```

Now let’s install all the dependencies and dev dependencies for this project. Run the following command to install all the dependencies.

```
pnpm i --save @apollo/server @nestjs/apollo @nestjs/config @nestjs/graphql @nestjs/mongoose class-transformer class-validator graphql graphql-kafkajs-subscriptions graphql-subscriptions graphql-ws kafkajs mongoose
```

In order for the subscriptions to work, we have to add the following to the `tsconfig.json` file.

```
{  
  "compilerOptions": {  
    "lib": ["ESNext.AsyncIterable", "DOM"]  
  }  
}
```

## Setup

First, modify the `main.ts` file as follows. This way we can clearly see, where the nestjs server, graphql server and the web socket for graphql subscriptions is listening.

```
import { NestFactory } from '@nestjs/core';  
import { AppModule } from './app.module';  
  
async function bootstrap() {  
  const app = await NestFactory.create(AppModule);  
  
  const port = 4000;  
  const url = `localhost:${port}`;  
  
  await app.listen(port);  
  
  console.log(`🚀  Server ready at: http://${url}`);  
  console.log(`🚀  GraphQL API ready at: http://${url}/graphql`);  
  console.log(`🚀  GraphQL subscriptions ready at: ws://${url}/graphql`);  
}  
  
bootstrap();
```

Create a file `src/config/configuration.ts` to load the configurations needed for GraphQL and Mongoose modules. This way is better, as it enables to use environment variables.

```
export default () => ({  
    port: parseInt(process.env.PORT, 10) || 4000,  
    database: {  
        url: process.env.DATABASE_URL || "mongodb://localhost:27017"  
    },  
});
```

In the `app.module.ts` file, let’s configure the Moongoose and GraphQL modules.

```
import { Module } from '@nestjs/common';  
import { AppController } from './app.controller';  
import { AppService } from './app.service';  
import { MongooseModule } from '@nestjs/mongoose';  
import { ApolloDriverConfig, ApolloDriver } from '@nestjs/apollo';  
import { GraphQLModule } from '@nestjs/graphql';  
import { join } from 'path';  
  
@Module({  
  imports: [  
    MongooseModule.forRootAsync({  
      useFactory: async () => ({  
        uri: 'mongodb://localhost:27017', // add your database uri here  
      }),  
    }),  
  
    GraphQLModule.forRoot<ApolloDriverConfig>({  
      driver: ApolloDriver,  
      playground: true,  
      autoSchemaFile: join(process.cwd(), 'src/graphql/schema.gql'),  
      subscriptions: {  
        'graphql-ws': true, // this enables graphql subscriptions  
      },  
      include: [] // here we need to include relevent modules with entities that we need to consider for the graphql schema  
    }),  
  ],  
  controllers: [AppController],  
  providers: [AppService],  
})  
export class AppModule {}
```

Make sure to create the `src/graphql/schema.gql` file. This is needed for the GraphQL module as it will be used to save the generated schema.

At this point if we try to start the server using `pnpm start:dev` we see an error as follows. This is because, in code-first approach, graphql requires at least one `query` to start the schema generation.

```
[8:19:23 PM] Starting compilation in watch mode...  
  
[8:19:26 PM] Found 0 errors. Watching for file changes.  
  
[Nest] 28216  - 03/12/2024, 8:19:27 PM     LOG [NestFactory] Starting Nest application...  
[Nest] 28216  - 03/12/2024, 8:19:27 PM     LOG [InstanceLoader] MongooseModule dependencies initialized +14ms  
[Nest] 28216  - 03/12/2024, 8:19:27 PM     LOG [InstanceLoader] ConfigHostModule dependencies initialized +1ms  
[Nest] 28216  - 03/12/2024, 8:19:27 PM     LOG [InstanceLoader] AppModule dependencies initialized +0ms  
[Nest] 28216  - 03/12/2024, 8:19:27 PM     LOG [InstanceLoader] ConfigModule dependencies initialized +0ms  
[Nest] 28216  - 03/12/2024, 8:19:27 PM     LOG [InstanceLoader] ConfigModule dependencies initialized +0ms  
[Nest] 28216  - 03/12/2024, 8:19:27 PM     LOG [InstanceLoader] GraphQLSchemaBuilderModule dependencies initialized +10ms  
[Nest] 28216  - 03/12/2024, 8:19:27 PM     LOG [InstanceLoader] GraphQLModule dependencies initialized +0ms  
[Nest] 28216  - 03/12/2024, 8:19:28 PM     LOG [InstanceLoader] MongooseCoreModule dependencies initialized +1572ms  
[Nest] 28216  - 03/12/2024, 8:19:28 PM     LOG [RoutesResolver] AppController {/}: +11ms  
[Nest] 28216  - 03/12/2024, 8:19:28 PM     LOG [RouterExplorer] Mapped {/, GET} route +2ms  
[  
  GraphQLError: Query root type must be provided.  
...
```

Press enter or click to view image in full size

![]()

## Transform Your Vision into a Stunning Website!

Professional Web Development Services on Fiverr

Boost your online presence with a custom website tailored to your needs. Whether it’s for a business, portfolio, or personal project, **I deliver top-notch web development** with fast turnaround times.

Get Started Today!

[🔗 Hire Me on Fiverr](https://www.fiverr.com/s/qD88jRg)

## GraphQL an MongoDB Schema

Let’s create a `post` entity before we begin with the subscription implementation. Using the nest cli, we can generate the modules, services and resolvers for this entity.

```
nest g mo post  
nest g s post  
nest g r post
```

We will also have to manually create the rest of the dto and entity files as follows. These are **required** for graphql resolvers and schema generation.

Press enter or click to view image in full size

![]()

Create the `post.ts` which defines the structure of the entity, graphql object type and the mongodb schema.

```
import { Field, ID, ObjectType } from "@nestjs/graphql";  
import { Prop, Schema, SchemaFactory } from "@nestjs/mongoose";  
import { Document, Types } from "mongoose";  
  
@ObjectType()  
@Schema({ timestamps: true })  
export class Post extends Document {  
    @Field(() => ID)  
    @Prop({ default: () => new Types.ObjectId() })  
    _id: Types.ObjectId;  
  
    @Field(() => Date)  
    @Prop()  
    createdAt: Date;  
  
    @Field(() => Date)  
    @Prop()  
    updatedAt: Date;  
  
    @Field(() => Date, { nullable: true })  
    @Prop()  
    deletedAt?: Date;  
  
    @Field()  
    @Prop()  
    title: string;  
  
    @Field({ nullable: true })  
    @Prop()  
    description?: string;  
}  
  
export const PostSchema = SchemaFactory.createForClass(Post);
```

The `post.create.ts` , `post.update.ts` , `post.filter.ts` files will define the graphql input types for the resolvers.

```
// post.create.ts  
import { InputType, Field } from '@nestjs/graphql';  
  
@InputType()  
export class CreatePostInput {  
  @Field()  
  title: string;  
  
  @Field({ nullable: true })  
  description?: string;  
}
```

```
// post.update.ts  
import { InputType, Field } from '@nestjs/graphql';  
  
@InputType()  
export class UpdatePostInput {  
  @Field({ nullable: true })  
  title?: string;  
  
  @Field({ nullable: true })  
  description?: string;  
}
```

```
// post.filter.ts  
import { InputType, Field } from '@nestjs/graphql';  
  
@InputType()  
export class FilterPostInput {  
    @Field({ nullable: true })  
    title?: string;  
  
    @Field({ nullable: true })  
    description?: string;  
}
```

The `post.service.ts` file defines the logic for the crud operations for the `post` entity,

```
import { Injectable } from '@nestjs/common';  
import { Model } from 'mongoose';  
import { InjectModel } from '@nestjs/mongoose';  
import { Post } from './post';  
  
@Injectable()  
export class PostService {  
  constructor(  
    @InjectModel(Post.name)  
    private model: Model<Post>,  
  ) {}  
  
  async getTotalCount(filters: Record<string, any>): Promise<number> {  
    const totalCount = await this.model.countDocuments(filters).exec();  
    return totalCount;  
  }  
  
  async findOneById(id: string): Promise<Post | null> {  
    if (id) {  
      return this.model.findById(id).exec();  
    }  
    return null;  
  }  
  
  async findAll(  
    pageNumber: number,  
    pageSize: number,  
    filters: Record<string, any>,  
  ): Promise<Post[] | null> {  
    const skipCount = (pageNumber - 1) * pageSize;  
  
    return this.model  
      .find()  
      .where(filters)  
      .skip(skipCount)  
      .limit(pageSize)  
      .exec();  
  }  
  
  async create(input: Partial<Post>): Promise<Post> {  
    const created = new this.model(input);  
    return created.save();  
  }  
  
  async update(id: string, input: Partial<Post>): Promise<Post | null> {  
    const existing = await this.model.findById(id).exec();  
  
    if (!existing) {  
      // Handle the case where the input with the given ID is not found  
      return null;  
    }  
  
    return this.model.findByIdAndUpdate(id, input, { new: true }).exec();  
  }  
  
  async delete(id: string, softDelete: boolean = false): Promise<Post | null> {  
    if (softDelete) {  
      // Soft delete by marking as deleted (assuming 'deletedAt' field exists in the schema)  
      return this.model  
        .findByIdAndUpdate(id, { deletedAt: new Date() }, { new: true })  
        .exec();  
    } else {  
      // Hard delete  
      return this.model.findByIdAndDelete(id).exec();  
    }  
  }  
}
```

and here’s the `post.resolver.ts` file.

```
import {  
  Args,  
  Int,  
  Mutation,  
  Parent,  
  Query,  
  ResolveField,  
  Resolver,  
  Subscription,  
} from '@nestjs/graphql';  
import { Post } from './post';  
import { PostService } from './post.service';  
import { FilterPostInput } from './post.filter';  
import { CreatePostInput } from './post.create';  
import { UpdatePostInput } from './post.update';  
  
@Resolver(() => Post)  
export class PostResolver {  
  constructor(  
    private postService: PostService,  
  ) {}  
  
  @Query(() => Int)  
  async totalPostCount(  
    @Parent() posts: Post[],  
    @Args('filters', { type: () => FilterPostInput, nullable: true })  
    filters?: FilterPostInput,  
  ): Promise<number> {  
    const totalCount = await this.postService.getTotalCount(filters);  
    return totalCount;  
  }  
  
  @Query(() => Post)  
  async post(@Args('id') id: string): Promise<Post | null> {  
    return this.postService.findOneById(id);  
  }  
  
  @Query(() => [Post])  
  async posts(  
    @Args('pageNumber', { type: () => Int }) pageNumber: number,  
    @Args('pageSize', { type: () => Int }) pageSize: number,  
    @Args('filters', { type: () => FilterPostInput, nullable: true })  
    filters?: any,  
  ): Promise<Post[] | null> {  
    return this.postService.findAll(pageNumber, pageSize, filters);  
  }  
  
  @Mutation(() => Post)  
  async createPost(  
    @Args('post') post: CreatePostInput,  
  ): Promise<Post> {  
    return this.postService.create(post);  
  }  
  
  @Mutation(() => Post)  
  async updatePost(  
    @Args('id') id: string,  
    @Args('post') post: UpdatePostInput,  
  ): Promise<Post | null> {  
    return this.postService.update(id, post);  
  }  
  
  @Mutation(() => Post)  
  async deletePost(  
    @Args('id') id: string,  
    @Args('softDelete', { nullable: true, defaultValue: false })  
    softDelete: boolean,  
  ): Promise<Post | null> {  
    return this.postService.delete(id, softDelete);  
  }  
}
```

Now to connect all the resolvers and services, we have to modify the `post.module.ts` file as follows,

```
import { Module } from '@nestjs/common';  
import { MongooseModule } from '@nestjs/mongoose';  
import { Post, PostSchema } from './post';  
import { PostResolver } from './post.resolver';  
import { PostService } from './post.service';  
  
@Module({  
  imports: [  
    MongooseModule.forFeature([{  
      name: Post.name,  
      schema: PostSchema  
    }]),  
  ],  
  providers: [PostResolver, PostService],  
  exports: [PostService],  
})  
export class PostModule { }
```

and add it to the `app.module.ts` file.

```
import { Module } from '@nestjs/common';  
import { AppController } from './app.controller';  
import { AppService } from './app.service';  
import { ApolloDriverConfig, ApolloDriver } from '@nestjs/apollo';  
import { GraphQLModule } from '@nestjs/graphql';  
import { MongooseModule } from '@nestjs/mongoose';  
import { ConfigModule, ConfigService } from '@nestjs/config';  
import configuration from './config/configuration';  
import { join } from 'path';  
import { PostModule } from './post/post.module'; // import the post module  
  
@Module({  
  imports: [  
    ConfigModule.forRoot({  
      load: [configuration]  
    }),  
  
    MongooseModule.forRootAsync({ // config }),  
  
    GraphQLModule.forRoot<ApolloDriverConfig>({  
      // other config  
      include: [PostModule] // add the post module into the 'include' for schema generation  
    }),  
  
    PostModule, // add the post module into the imports  
  ],  
  controllers: [AppController],  
  providers: [AppService],  
})  
export class AppModule { }
```

Now, when we run the sever, we can se the following output.

```
[8:41:57 PM] File change detected. Starting incremental compilation...  
  
[8:41:57 PM] Found 0 errors. Watching for file changes.  
  
[Nest] 3684  - 03/12/2024, 8:41:58 PM     LOG [NestFactory] Starting Nest application...  
[Nest] 3684  - 03/12/2024, 8:41:58 PM     LOG [InstanceLoader] MongooseModule dependencies initialized +13ms  
[Nest] 3684  - 03/12/2024, 8:41:58 PM     LOG [InstanceLoader] ConfigHostModule dependencies initialized +1ms  
[Nest] 3684  - 03/12/2024, 8:41:58 PM     LOG [InstanceLoader] AppModule dependencies initialized +0ms  
[Nest] 3684  - 03/12/2024, 8:41:58 PM     LOG [InstanceLoader] ConfigModule dependencies initialized +2ms  
[Nest] 3684  - 03/12/2024, 8:41:58 PM     LOG [InstanceLoader] ConfigModule dependencies initialized +0ms  
[Nest] 3684  - 03/12/2024, 8:41:58 PM     LOG [InstanceLoader] GraphQLSchemaBuilderModule dependencies initialized +9ms  
[Nest] 3684  - 03/12/2024, 8:41:58 PM     LOG [InstanceLoader] GraphQLModule dependencies initialized +1ms  
[Nest] 3684  - 03/12/2024, 8:42:00 PM     LOG [InstanceLoader] MongooseCoreModule dependencies initialized +1789ms  
[Nest] 3684  - 03/12/2024, 8:42:00 PM     LOG [InstanceLoader] MongooseModule dependencies initialized +5ms  
[Nest] 3684  - 03/12/2024, 8:42:00 PM     LOG [InstanceLoader] PostModule dependencies initialized +0ms  
[Nest] 3684  - 03/12/2024, 8:42:00 PM     LOG [RoutesResolver] AppController {/}: +12ms  
[Nest] 3684  - 03/12/2024, 8:42:00 PM     LOG [RouterExplorer] Mapped {/, GET} route +1ms  
[Nest] 3684  - 03/12/2024, 8:42:00 PM     LOG [GraphQLModule] Mapped {/graphql, POST} route +70ms  
[Nest] 3684  - 03/12/2024, 8:42:00 PM     LOG [NestApplication] Nest application successfully started +1ms  
🚀  Server ready at: http://localhost:4000  
🚀  GraphQL API ready at: http://localhost:4000/graphql  
🚀  GraphQL subscriptions ready at: ws://localhost:4000/graphql
```

The generated graphql schema will look like this.

```
# ------------------------------------------------------  
# THIS FILE WAS AUTOMATICALLY GENERATED (DO NOT MODIFY)  
# ------------------------------------------------------  
  
type Post {  
  _id: ID!  
  createdAt: DateTime!  
  updatedAt: DateTime!  
  deletedAt: DateTime  
  title: String!  
  description: String  
}  
  
"""  
A date-time string at UTC, such as 2019-12-03T09:54:33Z, compliant with the date-time format.  
"""  
scalar DateTime  
  
type Query {  
  totalEmployeesCount(filters: FilterPostInput): Int!  
  employee(id: String!): Post!  
  
  """Get all employees"""  
  employees(pageNumber: Int!, pageSize: Int!, filters: FilterPostInput): [Post!]!  
}  
  
input FilterPostInput {  
  title: String  
  description: String  
}  
  
type Mutation {  
  createEmployee(employee: CreatePostInput!): Post!  
  updateEmployee(id: String!, employee: UpdatePostInput!): Post!  
  deleteEmployee(id: String!, softDelete: Boolean = false): Post!  
}  
  
input CreatePostInput {  
  title: String!  
  description: String  
}  
  
input UpdatePostInput {  
  title: String  
  description: String  
}
```

You will also see a new collection called `posts` in your mongodb database.

## Subscriptions

Now we are ready to implement GraphQL subscriptions!

First we need to start an Apache Kafka server. You can use either zookeeper, kraft or docker. I will be using docker for this project. Feel free to refer to this [Apache Kafka](https://kafka.apache.org/quickstart) guide for more information.

```
docker pull apache/kafka:3.7.0  
docker run -p 9092:9092 apache/kafka:3.7.0
```

Once the Kafka server has successfully launched, you will have a basic Kafka environment running and ready to use.

Create a new `pubsub.module.ts` using the nest cli.

```
nest g mo pubsub
```

Create a `kafka.pubsub.service.ts` file inside the `src/pubsub/` folder.

```
import { Injectable, OnModuleInit } from '@nestjs/common';  
import { Kafka, logLevel } from 'kafkajs';  
import { KafkaPubSub } from 'graphql-kafkajs-subscriptions';  
  
@Injectable()  
export class KafkaPubSubService implements OnModuleInit {  
  private pubsub: KafkaPubSub;  
  
  constructor() {}  
  
  async onModuleInit() {  
    await this.initializePubSub();  
  }  
  
  private async initializePubSub(): Promise<void> {  
    const kafka = new Kafka({  
      logLevel: logLevel.ERROR,  
      clientId: 'ngk', // this doesn't matter. feel free to have any unqiue name  
      brokers: ['localhost:9092'], // add your kafka broker uri with the correct port  
      connectionTimeout: 25000,  
      retry: {  
        retries: 3,  
        maxRetryTime: 3000,  
      },  
    });  
  
    this.pubsub = await KafkaPubSub.create({  
      kafka,  
      topic: 'ngk-event',  
      groupIdPrefix: 'ngk-group',  
    });  
  }  
  
  getPubSub(): KafkaPubSub {  
    if (!this.pubsub) {  
      throw new Error('PubSub is not initialized');  
    }  
    return this.pubsub;  
  }  
}
```

Modify the `pubsub.module.ts` file as follows and expose the kafka pubsub service.

```
import { Module } from '@nestjs/common';  
import { KafkaPubSubService } from './kafka.pubsub.service';  
  
@Module({  
    providers: [KafkaPubSubService],  
    exports: [KafkaPubSubService]  
})  
export class PubsubModule {}
```

To use the `pubsub`module with the `post` module, we have to import it as follows.

```
import { Module } from '@nestjs/common';  
import { MongooseModule } from '@nestjs/mongoose';  
import { Post, PostSchema } from './post';  
import { PostResolver } from './post.resolver';  
import { PostService } from './post.service';  
import { PubsubModule } from 'src/pubsub/pubsub.module'; // import the file  
  
@Module({  
  imports: [  
    PubsubModule, // add this line  
  
    MongooseModule.forFeature([{  
      name: Post.name,  
      schema: PostSchema  
    }]),  
  ],  
  providers: [PostResolver, PostService],  
  exports: [PostService],  
})  
export class PostModule { }
```

To subscribe, we need to publish a message. In the `createPost` resolver in `post.resolver.ts`, use the kafka pubsub we created and publish the newly created `post` to a channel.

```
  @Mutation(() => Post)  
  async createPost(@Args('post') post: CreatePostInput): Promise<Post> {  
    const created = await this.postService.create(post);  
  
    await this.pubsubService.getPubSub().publish(  
      'postCreated', // channel / topic  
      JSON.stringify({  
        postCreated: created,  
      }), // when publishing the message, the payload must first be serialized.  
    );  
  
    return created;  
  }
```

To listen to the published message, we need a subscription. Create a subscription as follows in the same file. *(This is only for demonstration. In real world scenario, we would have something like, creating a* `post`*, publishing it to a channel/group, and all the* `users` *will get a notification about the newly created* `post` *. To implement something similar, we need to create a* `user` *entity along with the relevant resolvers, services, input types. The* `@Subscription` *will be defined inside the* `user.resolver.ts`*)*

```
  @Subscription(() => Post, {  
    resolve(payload, args, context, info) {  
      // Convert the Buffer to a string and parse the JSON  
      const jsonString = payload?.value?.toString('utf-8');  
      const parsedPayload = JSON.parse(jsonString);  
      const postCreated = parsedPayload?.postCreated;  
  
      if (postCreated) {  
        postCreated.createdAt = new Date(postCreated.createdAt);  
        postCreated.updatedAt = new Date(postCreated.updatedAt);  
      }  
  
      return postCreated;  
    },  
  })  
  async postCreated() {  
    return this.pubsubService  
      .getPubSub()  
      .asyncIterator('postCreated');  
  }
```

## Let’s see it in Action!

I’m using [**Altair GraphQL Client**](https://altairgraphql.dev/#download)to test the subscriptions. Feel free to use the GraphQL playground or any other preferred way.

Start the server using `pnpm start:dev`

Open the GraphQL client and open tabs: one for the `createPost` mutation and the other for the `postCreated` subscription. Execute the mutation and see the subscription tab. Note how you instantly get a notification about the newly created post.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

This is how you implement a GraphQL subscription backed with Apache Kafka in NestJS. To learn more about how to filter, or resolve the subscriptions, check the official docs in [GraphQL + TypeScript — Subscriptions | NestJS — A progressive Node.js framework](https://docs.nestjs.com/graphql/subscriptions)

You can download the source code from this GitHub repo. <https://github.com/kodiidok/nestjs-graphql-pubsub-kafka.git>

## In Plain English 🚀

*Thank you for being a part of the* [***In Plain English***](https://plainenglish.io) *community! Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://twitter.com/inPlainEngHQ) **|** [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) **|** [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) **|** [**Discord**](https://discord.gg/in-plain-english-709094664682340443) **|** [**Newsletter**](https://newsletter.plainenglish.io/)
* Visit our other platforms: [**Stackademic**](https://stackademic.com/) **|** [**CoFeed**](https://cofeed.app/) **|** [**Venture**](https://venturemagazine.net/) **|** [**Cubed**](https://blog.cubed.run)
* More content at [**PlainEnglish.io**](https://plainenglish.io)