# Docker Stuff

In this article we will look at Docker. Since containers became popular, many people have asked about them, and as we discussed in part one, there is a lot of history here going back to chroot and BSD jails and the early days of virtualization, which is a fascinating story that I think everyone should know about because it explains so much about where we are today and why things are the way they are in the modern cloud native ecosystem.

## Overview

Docker is simply a powerful frontend to cgroups. Obviously you know what that means. See [here](https://docs.docker.com) for more.

```
docker run -it ubuntu bash
```

## Conclusion

It's easy once you get it.
