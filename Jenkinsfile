pipeline {
    agent any      // agent {label 'default'}

    environment {
        PROJECT_ID = 'ptoject1-424215'
        CLUSTER_NAME = 'autopilot-cluster-1'
        LOCATION = 'asia-south1'
        CREDENTIALS = 'gcp-key'
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
                git credentialsId:"github-token", url:"https://github.com/rajatvegan/UNITY.git", branch: "main"
            }
        }

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

        // stage("Deploy"){
        //     steps {
        //         echo "Deploying the container"
        //         sh "docker-compose down && docker-compose up -d"
                
        //     }
        // }

        // stage("deploy to aws eks"){
        //     steps {
        //         echo "connecting to eks cluster"
        //         script{sh "aws eks update-kubeconfig --name eks-cluster1"}
        //         echo "deploying the pods on eks"
        //         script{sh "kubectl apply -f deployment-service.yml"}
        //     }
        // }

        stage("deploy to gcp k8s"){
            steps {
                echo "deploying the dockerhub image on gke"
                step([$class:'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'deployment-service.yml', credentialsId: env.CREDENTIALS, verifyDeployments: true ])
            }
        }



    }
}