pipeline {
    agent any
    stages {
		stage('Stage: Poll SCM') {
			steps {
				triggers { pollSCM('H */4 * * 1-5') }
			}
		}
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
		stage('Stage: Packaging') {
			steps {
				echo 'Packaging the Projects ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn package'
				}
			}
		}
    }
}
