pipeline {
    agent any
    tools {
        jdk 'java17'
        maven 'maven3'
    }

    
    stages{
        stage('Cleanup Workspace'){
            steps{
                cleanWs()
            }
        }

        stage("Clone Code"){
            steps {
                echo "Cloning the code"
                git credentialsId:"gith", url:"https://github.com/rajatvegan/UNITY.git", branch: "main"
            }
        }

        stage('Build Application'){
            steps{
                sh "mvn clean package"
            }
        }

        stage('Test Apllication'){
            steps{
                sh "mvn test"
            }
        }

        // stage("Build"){
        //     steps {
        //         echo "Building the image"
        //         sh "docker build -t unity-app ."
        //     }
        // }

        // stage("Push to Docker Hub"){
        //     steps {
        //         echo "Pushing the image to docker hub"
        //         withCredentials([usernamePassword(credentialsId:"dockerHub",passwordVariable:"dockerHubPass",usernameVariable:"dockerHubUser")]){
        //         sh "docker tag unity-app ${env.dockerHubUser}/unity-app:latest"
        //         sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
        //         sh "docker push ${env.dockerHubUser}/unity-app:latest"
        //         }
        //     }
        // }

        // stage("Deploy"){
        //     steps {
        //         echo "Deploying the container"
        //         sh "docker-compose down && docker-compose up -d"
                
        //     }
        // }
    }
}