# Run any Linux tool without installing it, using Docker

If you've ever installed a tool to try it once and then spent an evening removing it, Docker solves that. In this post you'll run Ubuntu's shell in a throwaway container in one command. When you exit, nothing is left on your machine.

## One command gives you a disposable Ubuntu shell

Install Docker Desktop from docker.com, then run:

```
docker run -it --rm ubuntu bash
```

`docker run` starts a container from the `ubuntu` image, downloading it the first time. `-it` connects your keyboard and terminal to it, and `--rm` deletes the container when you exit. The prompt changes to `root@<id>:/#`, which tells you you're inside.

## Nothing you install inside survives the exit

Inside the container, install a package with `apt-get update && apt-get install -y cowsay`, run it, then type `exit`. Run the same `docker run` command again and `cowsay` is gone. Each run starts from the clean image.
