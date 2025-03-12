# Deployment Steps

1. **Update Strings:** Replace the contents of the `strings.ts` file located in the `lib/strings.ts` directory.
2. **Build Docker Image:** Build the Docker container using the command: `docker build -t juanjaragavi/quiz-topfinanzas:latest .`
3. **Push to Docker Hub:** Push the built image to Docker Hub with: `docker push juanjaragavi/quiz-topfinanzas:latest`
4. **Access Cloud Run:** In Google Cloud Platform (GCP), navigate to the Cloud Run service and select the `quiz-topfinanzas-com` service.
5. **Deploy New Version:** Click "Edit & Deploy New Version."
6. **Set Container Image URL:** In the "Container image URL" field, enter `docker.io/juanjaragavi/quiz-topfinanzas:latest`.
7. **Deploy:** Click "Deploy," leaving all other configuration options unchanged.
