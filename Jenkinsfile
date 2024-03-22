pipeline {
    agent {label 'default'}
    
    stages{
        stage('Cleanup Workspace'){
            steps{
                cleanWs()
            }
        }

        stage("Clone Code"){
            steps {
                echo "Cloning the code"
                git credentialsId:"github-token", url:"https://github.com/rajatvegan/UNITY.git", branch: "main"
            }
        }

        // stage("installing docker"){
        //     steps {
        //         sh "sudo apt install docker.io"
        //         sh "sudo apt install docker-compose"
        //     }
        // }

        stage("Build"){
            steps {
                echo "Building the image"
                sh "docker build -t unity-app ."
            }
        }

        stage("Push to Docker Hub"){
            steps {
                echo "Pushing the image to docker hub"
                withCredentials([usernamePassword(credentialsId:"dockerHub",passwordVariable:"dockerHubPass",usernameVariable:"dockerHubUser")]){
                sh "docker tag unity-app ${env.dockerHubUser}/unity-app:latest"
                sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                sh "docker push ${env.dockerHubUser}/unity-app:latest"
                }
            }
        }

        stage("Deploy"){
            steps {
                echo "Deploying the container"
                sh "docker-compose down && docker-compose up -d"
                
            }
        }

        stage("deploy to aws eks"){
            steps {
                echo "deploying the pods"
                sh "kubectl apply -f /var/lib/jenkins/workspace/declarative-pipeline/deployment-service.yml"
            }
        }
    }
}