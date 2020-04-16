## 1.基础使用
```jenkins
Jenkinsfile (Declarative Pipeline)
pipeline {
    agent { docker 'python:3.5.1' }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}
```
- `pipeline`由多个步骤组成  
- 每个步骤可以看成执行单一动作的单一命令
- 当有一个步骤执行失败时，`pipeline`失败
- 当所有步骤都执行成功，`pipeline`执行成功
- 在类unix系统中的shell命令，对应于`pipeline`中的`sh`步骤
- 在基于windows系统中，使用`bat`步骤表示执行批处理命令

### 1.1 超时与重试
```
steps {
    retry(3){
        sh './xxx.sh'
    }
    timeout(time:3, unit:'MINUTES'){
        sh './yyy.sh'
    }
}
```
- 重试执行`xxx.sh`脚本三次，直到成功
- 执行脚本`yyy.sh`若超过3分钟，则`pipeline`失败
- `retry`和`timeout`支持嵌套

### 1.2 完成时动作
```
Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'echo "Fail!"; exit 1'
            }
        }
    }
    post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}
```
- 在`pipeline`运行完成时，可能需要做一歇清理工作或者基于`pipeline`的运行结果执行不同的操作，这些操作可以放在`post`部分

### 1.3定义执行环境
- 每个`pipeline`中都有`agent`指令
- `agent`指令告诉Jenkins在哪里以及如何执行pipeline
- `agent`指令会使所有在block里二点步骤会被保存到一个执行队列，一旦一个执行器可用，将会开始执行
- 一个工作空间将会被分配，包含来自远程仓库的文件和一些用于pipeline的工作文件

### 1.4定义环境变量
- 环境变量可以设置为全局或者阶段级别的
```
Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
    }

    stages {
        stage('Build') {
            steps {
                sh 'printenv'
            }
        }
    }
}
```

### 1.5 清理和通知
- 因为`post`部分保证在`pipeline`结束时运行，因此可以添加通知或者其他的步骤完成清理、通知或其他的结束任务
```
Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any
    stages {
        stage('No-op') {
            steps {
                sh 'ls'
            }
        }
    }
    post {
        always {
            echo 'One way or another, I have finished'
            deleteDir() /* clean up our workspace */
        }
        success {
            echo 'I succeeeded!'
        }
        unstable {
            echo 'I am unstable :/'
        }
        failure {
            mail to: 'team@example.com',
            subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
            body: "Something is wrong with ${env.BUILD_URL}"
        }
        changed {
            echo 'Things were different before...'
        }
    }
}
```
- 除可以发送邮件外，还支持`hipchat`和`slack`

### 1.6部署及人工确认
```
Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any
    stages {
        /* "Build" and "Test" stages omitted */

        stage('Deploy - Staging') {
            steps {
                sh './deploy staging'
                sh './run-smoke-tests'
            }
        }

        stage('Sanity check') {
            steps {
                input "Does the staging environment look ok?"
            }
        }

        stage('Deploy - Production') {
            steps {
                sh './deploy production'
            }
        }
    }
}
```
- 阶段即为部署环境
- `Sanity check`阶段会等待直到人工确认，直到使用`input`步骤来完成人工的确认应用程序是否在一个足够好的状态

## 2.使用`Pyinstaller` 构建python应用
