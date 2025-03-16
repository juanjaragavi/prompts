# Prompt

Below, I am pasting a set of instructions to deploy a Next.js site in GCP's Cloud Run service after modifying a single file called `strings.ts`. We are running our code base, which is a Next.js project located in a folder called `quiz-topfinanzas-com`, in a GCP Compute Engine Ubuntu 22.04 VM Instance:

## Deployment Steps

1. **Update Strings:** Replace the contents of the `strings.ts` file located in the `lib/strings.ts` directory.
2. **Build Docker Image:** Build the Docker container using the command: `docker build -t juanjaragavi/quiz-topfinanzas:latest .`
3. **Push to Docker Hub:** Push the built image to Docker Hub with: `docker push juanjaragavi/quiz-topfinanzas:latest`
4. **Access Cloud Run:** In Google Cloud Platform (GCP), navigate to the Cloud Run service and select the `quiz-topfinanzas-com` service.
5. **Deploy New Version:** Click "Edit & Deploy New Version."
6. **Set Container Image URL:** In the "Container image URL" field, enter `docker.io/juanjaragavi/quiz-topfinanzas:latest`.
7. **Deploy:** Click "Deploy," leaving all other configuration options unchanged.

Our goal is to pass all of that workload to an LLM-based Agent, which will receive the `strings.ts` file as an output of a previous Agent in our Agentic Workflow (it is yet to be decided if the Agent will receive a text output, or a file) and, being placed at the `root` (or at a previously created `tmp` folder if the output obtained is the `strings.ts` typescript file) of the `quiz-topfinanzas-com` Next.js application, the Agent will:

1. Execute the command `sudo cp -a tmp/strings.ts lib/strings.ts` to replace the current `lib/strings.ts` file
2. Execute the command `sudo docker build -t juanjaragavi/quiz-topfinanzas:latest .` to build the Docker container
3. Execute the command `sudo docker.io/juanjaragavi/quiz-topfinanzas:latest` to push it to Docker Hub
4. Execute the command `sudo docker build -t juanjaragavi/quiz-topfinanzas:latest .` to build the Docker container and also execute the command `sudo docker.io/juanjaragavi/quiz-topfinanzas:latest` to push it to Docker Hub

## Task

Your task is to search online in multiple up-to-date information sources and, after your detailed research, prepare a detailed and comprehensive tutorial on how to perform this automation using LLMs, all of the GCP infrastructure, Flowise and n8n, which is our current tech stack.

## Important

- The Agent should have all of the permissions and privileges to execute those commands successfully
- It is imperative that the Agent should consider the pauses that need to be taken between commands, in order to allow them to be execute properly
