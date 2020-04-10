# Kafka 学习笔记及kafka-python的配合使用

## 1.基础知识
![架构图](https://atts.w3cschool.cn/attachments/tuploads/apache_kafka/fundamentals.jpg)

### 1.1主题`Topics`

- 特定的类别的消息成为主题，数据存储在主题中
- 主题被拆分成分区，对于每个分区， Kafka保存一个主题的数据

### 1.2分区`Pattition`
- 一个主题可能有多个分区， 因此它可以处理任意数量的数据
- 分区被实现为具有想等大小的一组分段文件
- 分区时消息的线性有序序列

### 1.3分区偏移`Pattition offset`
- 每个分区消息具有称为`offset`的唯一序列标识

### 1.4分区备份(Replicas of partition)
- 副本是分区的备份，不读写数据，用于防止数据丢失

### 1.5 代理(Broker)
- 代理是负责维护发布数据的简单系统
- 每个代理中的每个主题可以具有0或多个分区，并尽量保持负载均衡
- 假设一个主题中，代理多于分区数，则均匀的分配给前N个代理
- 假设一个主题中，代理数小于分区数，每个代理有一个或多个分区，由于无法保证负载的均衡，因此不推荐使用

### 1.6 Kafka集群（Kafka Cluster）
- Kafka有多个代理成为集群
- 可以不停机的扩展集群
- 集群用于管理消息数据的持久性和复制

### 1.7 生产者(Producer)
- 发送给一个或多个kafka主题消息的发布方称为生产者
- 生产者向kakfa代理发送数据，当代理收到消息时，只需将消息附加到最后一个段文件
- 实际上消息被附加到分区，生产给可以向特定的分区发送消息

### 1.8 消费者(Consumer)
- 消费者从代理读取数据
- 消费者订阅一个或多个主题， 并通过从代理中提取数据来使用已发布的消息

### 1.9 领导者(Leader)
- 领导者负责给定分区的所有读写节点
- 每个分区都有一个服务器充当领导者

### 1.10 追随者(Follower)
- 跟随领导者指令的节点称为追随者
- 如果领导者不可用， 一个追随者将自动称为新的领导者
- 追随者作为正常消费者，拉取消息并更新其自己的数据存储

## 2. Apache Kafka集群架构
![架构图](https://atts.w3cschool.cn/attachments/tuploads/apache_kafka/cluster_architecture.jpg)

### 2.1 代理
- Kafka集群通常由多个代理组成，以保持负载均衡
- Kafka代理是无状态的，因此使用`ZooKeeper`维护集群状态
- 代理的`leader`选举由`ZooKeeper`完成

### 2.2 ZooKeeper
- 用于管理和协调Kafka代理
- 主要用于通知生产者和消费者Kafka系统中存在任何新代理或代理失败
- ZooKeeper接收到代理的存在或失败通知，然后告知生产者、消费者采取并开始与其他代理来协调任务

### 生产者
- 生产者将数据推送给代理
- 新代理启动时， 所有生产者搜索它并自动向新代理发送消息
- 消息的发送不需等待代理的确认，并且发送速度与代理处理速度一样快

### 消费者
- 因为代理是无状态的，意味着消费者必须通过分区偏移来维护已经消耗消息的数量
- 如果消费者确认了消息偏移，代表已经消费了所有先前的消息
- 消费者向代理发出异步拉去请求，以具有准备好消耗的字节缓冲区
- 可以通过简单的提供偏移值来进行分区跳跃至分区的任一点
- 偏移值由ZooKeeper通知

## 3. Kafka工作流程

### 3.1发布订阅消息的工作流程

- 生产者定期向主题发送消息。
- Kafka代理存储为该特定主题配置的分区中的`所有消息`。 它确保消息在分区之间平等共享。 如果生产者发送两个消息并且有两个分区，Kafka将在第一分区中存储一个消息，在第二分区中存储第二消息。
- 消费者订阅特定主题。
- 一旦消费者订阅主题，Kafka将向消费者提供主题的当前偏移，并且还将偏移保存在Zookeeper系综中。
- 消费者将`定期请求`Kafka(如100 Ms)新消息。
- 一旦Kafka收到来自生产者的消息，它将这些消息转发给消费者。
- 消费者将收到消息并进行处理。
- 一旦消息被处理，消费者将向Kafka代理`发送确认`。
- 一旦Kafka收到确认，它将偏移更改为新值，并在Zookeeper中更新它。 由于偏移在Zookeeper中维护，消费者可以正确地读取下一封邮件，即使在服务器暴力期间。
- 以上流程将重复，直到消费者停止请求。
- 消费者可以随时回退/跳到所需的主题偏移量，并阅读所有后续消息。

### 3.2消费者组和其工作流程
#### 3.2.1消费者组
- 消费者组下可以有一个或多个消费者实例，其可以是一个进程，也可以是一个线程
- group.id是一个字符串，唯一标识一个消费者组
- 消费者组下订阅的主题下的每个分区只能分配给某个组下的一个消费者(当然该分区还可以被分配给其他组)

#### 3.2.2工作流程
- 生产者以固定间隔向某个主题发送消息
- Kafka存储在为该特定主题配置的分区中的所有消息，类似于前面的方案
- 单个消费者订阅特定主题，假设 Topic-01的GroupID为 Group-1 
- Kafka以与发布-订阅消息相同的方式与消费者交互，直到新消费者以相同的组ID订阅相同主题Topic-01
- 一旦新消费者到达，Kafka将其操作切换到共享模式，并在两个消费者之间共享数据
- 此共享将继续，直到用户数达到为该特定主题配置的分区数。
- 一旦消费者的数量超过分区的数量，新消费者将不会接收任何进一步的消息，直到现有消费者取消订阅
- 出现这种情况是因为Kafka中的每个消费者将被分配至少一个分区，并且一旦所有分区被分配给现有消费者，新消费者将必须等待。
- 此功能也称为使用者组。 同样，Kafka将以非常简单和高效的方式提供两个系统中最好的

## 4.与使用
- ### 4.1[安装](https://cloud.tencent.com/developer/article/1445102)
- ### 4.2使用 
`kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic tuzisir`
- 创建一个主题
- `--zookeeper`指定`zookeeper`端口
- `--replication-factor`指定备份数
- `--partitions`指定分区数
- `--topic`指定主题名

## 5.kafka-python

### 5.1消费者

```python
from kafka import KafkaConsumer, TopicPartition
import msgpack
consumer = KafkaConsumer("topic 1",  # 指定主题
                         group_id="group1",  # 加入用户组
                         bootstrap_servers='localhost:8888',
                         value_deserializer=msgpack.loads)  # 消息反序列化方法    
```
- 基础使用
- 对于协调者的全面支持需要配合使用支持分组API的kafka0.9+版本

```
# Manually assign a list of TopicPartitions to this consumer
consumer.assign([TopicPartition("foo", 2)])  # 手动指定主题及分区
```
- 手动指定分区， 如果一定调用过`KafkaConsumer.subscribe`则会抛出错误
- 手动指定无法使用用户组管理功能
- 每次调用都是覆盖更新，而不是增量更新

```# Subscribe to a list of topics, or a topic regex pattern.
consumer.subscribe(topics=[], pattern="", listener=None)  # 订阅主题， 可以使用正则
```
- 订阅主题，可选正则表达式
- 如果调用过`KafkaConsumer.assign`则会报错
- `listener` 可选， 会在重新均衡负载前和后被调用

```
for msg in consumer:
    ...
```
- 消费者被实现为一个迭代器，通过迭代或者`next()`获取下一条消息
```python
import collections

ConsumerRecord = collections.namedtuple("ConsumerRecord",
    ["topic", "partition", "offset", "timestamp", "timestamp_type",
     "key", "value", "headers", "checksum", "serialized_key_size", "serialized_value_size", "serialized_header_size"])

```
- `msg`时一个`kafka.consumer.fetcher.ConsumerRecord`对象, 暴露出一条消息的基本属性

```
# Get metrics on consumer performance
metrics = consumer.metrics()
```

### 5.2 生产者
```python
from kafka import KafkaProducer

producer = KafkaProducer(
                        bootstrap_servers="localhost:8888",
                        key_serializer=str.encode,
                        compression_type='gzip')
producer.send("topic1", b"some msg")
```
- `KafkaProducer`时线程安全的， 在多个线程中共享一个实例比创建多个实例要更快
- 生产者包含了一个未被传输消息的缓冲池和后台I/O线程，负责将消息转化为请求并传输到集群
- `send`函数是异步的，返回一个Future实例，当调用时会将消息加入到缓冲区并迅速返回
- 如果发送失败，生产者会自动重试，除非重试被配置为0
- `acks`配置影响请求的完成， `all`配置会影响消息的完全提交
- 生产者为每个分区维护一个未发送消息的缓冲，缓冲区有大小配置`batch_size`，配置大的数需要更大的内存
- 通常缓冲会被立即发送即便缓冲区仍有空余，但是配置`linger_ms`配置大于0的数可以让生产者等待该毫秒数让更多的消息进来，一次发送
- 当消息发送量巨大时，会忽略`linger_ms`配置，并立即发送
- `buffer_memory`参数控制了生产者缓冲的总可用内存，如果发送速度大于传输速度，那么缓冲空间就会耗尽，此使新加入的发送会被阻塞
- `compression_type`指定了消息压缩的算法

```
future = producer.send("topic1", b"some msg")
result = future.get(timeout=60)
```

- 阻塞直到当前消息被发送


`producer.flush()`

- 阻塞至少被放到网络上，但并不保证传输一定成功
- 仅当配置了`linger_ms`时有效

`producer.send('foobar', key=b'foo', value=b'bar')`
- `key`指定发送到某一分区，若为空则随机发送
- 必须为bytes类型，或者可以被`key_serializer`序列化为bytes类型
- `key_serializer`在初始化生产者时配置`KafkaProducer(key_serializer=str.encode)`

```
import json
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer.send('fizzbuzz', {'foo': 'bar'}
```
- 指定消息的序列化方法

`producer.send('foobar', value=b'c29tZSB2YWx1ZQ==', headers=[('content-encoding', b'base64')])`
- 添加消息头

## 6.Kafka与[Storm](https://www.w3cschool.cn/apache_storm)
### 6.1 Storm基本概念
- `Tuple` 元组Storm的主要数据结构，默认情况下，支持所有数据类型，通常被建模为一组逗号分割的值，并传递到Storm集群
- `Stream` 流是元组的无序序列
- `Spouts` 流的源，可以从`StramingAPI`、`Kafka`、`Kestre`接收数据，或自己实现从数据源读取数据
- `ISpout` 是实现`spouts`是的核心接口。还有特定的接口IRichSpout，BaseRichSpout，KafkaSpout等
- `Bolts` 逻辑处理单元，`Spouts`将数据传递到`Bolts`，并产生新的输出流
- `Bolts` 可执行过滤、聚合、加入、与数据源和数据库交互等操作
- `IBolt` 是实现`Bolts`的核心接口。常见的接口有IRichBolt，IBasicBolt等。
- `拓扑` Spouts与Bolts连接在一起，形成拓扑结构，实时应用程序应在拓扑中指定，拓扑是有向图，其中顶点是计算，边缘是数据流
- 简单拓扑从spouts开始。Spouts将数据发射到一个或多个Bolts。
- Bolts的输出可以发射到另一个Bolts作为输入。
- Storm保持拓扑始终运行，直到您终止拓扑。
- Storm的主要工作是运行拓扑，并在给定时间运行任意f数量的拓扑。
- `任务` Storm执行的每个Spout和Bolt称为任务。
- 每个Spout和Bolt可以具有在多个单独的螺纹中运行的多个实例。
- 拓扑在多个工作节点上以分布式运行，Storm将所有工作节点上的任务均匀分布，工作节点的角色是监听作业，并在作业到达时启动或停止进程
- `流分组` 数据流从Spouts到Bolts，或从一个Bolt到另一个Bolt， 流分组控制元组在拓扑中的路由方式，并帮助了解拓扑中的元组流。
- 流分组的四个内置分组方式：随机分组、字段分组、全局分组、所有分组
- 随机分组 相等数量的元组随机分布在所有的Bolts中

![随机分组](https://atts.w3cschool.cn/attachments/tuploads/apache_storm/shuffle_grouping.jpg)
- 字段分组 具有相同字段值的元组被发送到用以Bolts进程

![字段分组](https://atts.w3cschool.cn/attachments/tuploads/apache_storm/field_grouping.jpg)
- 全局分组 所有流可以分组并向前到一个Bolts。此分组将源的所有实例生成的元组发送到单个目标实例(id值最低的实例)

![全局分组](https://atts.w3cschool.cn/attachments/tuploads/apache_storm/global_grouping.jpg)
- 所有分组 所有分组将每个元组的单个副本发送到接收Bolts的所有实例。这种分组用于向Bolts发送信号。所有分组对于连接操作都很有用。

![所有分组](https://atts.w3cschool.cn/attachments/tuploads/apache_storm/all_grouping.jpg)

### 6.2 Storm集群架构
- 架构图

![](https://atts.w3cschool.cn/attachments/tuploads/apache_storm/zookeeper_framework.jpg)
- Storm有两种类型的节点，Nimbus（主节点）和Supervisor（工作节点）
- Nimbus的主要工作是运行Storm拓扑。Nimbus分析拓扑并收集要执行的任务。然后，它将任务分配给可用的supervisor
- Supervisor将有一个或多个工作进程并将任务委派给工作进程。
- 工作进程将根据需要产生尽可能多的执行器并运行任务
- 执行器只是工作进程产生的单个线程。执行器运行一个或多个任务，但仅用于特定的spout或bolt。
- Nimbus是无状态的，所以它依赖于ZooKeeper来监视工作节点的状态

### 6.3 Storm工作流程
- nimbus将等待“Storm拓扑”提交给它。
- 一旦提交拓扑，它将处理拓扑并收集要执行的所有任务和任务将被执行的顺序。
- 然后，nimbus将任务均匀分配给所有可用的supervisors。
- 在特定的时间间隔，所有supervisor将向nimbus发送心跳以通知它们仍然运行着。
- 当supervisor终止并且不向心跳发送心跳时，则nimbus将任务分配给另一个supervisor。
- 当nimbus本身终止时，supervisor将在没有任何问题的情况下对已经分配的任务进行工作。
- 一旦所有的任务都完成后，supervisor将等待新的任务进去。
- 同时，终止nimbus将由服务监控工具自动重新启动。
- 重新启动的网络将从停止的地方继续。同样，终止supervisor也可以自动重新启动。由于网络管理程序和supervisor都可以自动重新启动，并且两者将像以前一样继续，因此Storm保证至少处理所有任务一次。
- 一旦处理了所有拓扑，则网络管理器等待新的拓扑到达，并且类似地，管理器等待新的任务。
- 默认情况下，Storm集群中有两种模式：
- 本地模式 -此模式用于开发，测试和调试，因为它是查看所有拓扑组件协同工作的最简单方法。在这种模式下，我们可以调整参数，使我们能够看到我们的拓扑如何在不同的Storm配置环境中运行。在本地模式下，storm拓扑在本地机器上在单个JVM中运行。
- 生产模式 -在这种模式下，我们将拓扑提交到工作Storm集群，该集群由许多进程组成，通常运行在不同的机器上。如在storm的工作流中所讨论的，工作集群将无限地运行，直到它被关闭。

### 6.4 Storm开启流程
- mac版配置文件在`/usr/local/Cellar/storm/1.2.3/libexec/conf/storm.yaml`
```yaml
storm.zookeeper.servers:
    - "127.0.0.1"
#     - "server2"
```
- 配置zookeeper地址

`nimbus.seeds: ["127.0.0.1"]`
- 配置用于发现nimbus leader

`storm nimbus`
- 启动`nimbus`

`storm supervisor`
- 启动`supervisor`

`storm ui`
- 启动webUI页面，默认端口8080

## 7.Kafka与Spark