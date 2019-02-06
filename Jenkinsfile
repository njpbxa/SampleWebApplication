pipeline {
    agent any
    stages {
		stage('Stage: Compile') {
			steps {
				echo 'Compiling the Projects ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn clean compile'
				}
			}
		}
		stage('Stage: Unit Test') {
			steps {
				echo 'Running Unit Tests ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn test'
				}
			}
		}
		
		stage('Stage: SonarQube Analysis') {
			steps {
				withSonarQubeEnv('sonarqube') {
                    withMaven(maven:'maven_3_6_0') {
                        sh 'mvn sonar:sonar'
                    }
                }
			}
		}

		stage("Stage: Quality Gate") {
			steps {
				timeout(time:5, unit:'MINUTES'){
					sleep(10)
					waitForQualityGate abortPipeline:true
				}
			}
		}
		
		stage('Stage: Packaging') {
			steps {
				echo 'Packaging the Projects ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn package'
				}
			}
		}
		lock{
		stage('Stage: Deploy in WAS') {
			steps {
				echo 'Deploying in WAS ..............'
				build job: 'DeployToWAS', parameters: [string(name: 'WAR_LOC', value: 'PipelineByAlakD/target/*.war'), string(name: 'APP_NAME', value: 'SampleWebApplication')]
			}
		}
		}
    }
}
