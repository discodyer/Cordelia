# Cordelia

A Telegram bot based on NoneBot2.

## Local development

1. generate project using `nb create` .
2. install plugins using `nb plugin install` .
3. run your bot using `nb run` .

## Docker 部署

镜像运行 NoneBot 的 ASGI 应用。先复制示例配置，填写 Telegram Bot Token：

```bash
cp .env.example .env
# 编辑 .env，填写 Telegram token 等配置
docker compose up -d --build
docker compose logs -f cordelia
```

默认使用 Telegram 轮询，容器不需要映射端口。

Compose 将同一份配置注入环境变量并只读挂载到 `/app/.env`。NoneBot 2.5
需要从 dotenv 文件发现 `telegram_bots` 和插件自定义配置项，仅设置环境变量
会导致这些配置未被加载。未配置 bot 时应用会明确报错并退出。

## GitHub Actions + self-hosted runner 自动部署

每次推送到 `main`，工作流会在服务器上的 runner 执行 `actions/checkout` 拉取该提交，
构建新镜像，再用 Docker Compose 更新容器。runner 主动连接 GitHub，因此服务器
无需公网 IP，也无需开放入站端口。

### 服务器首次配置

安装 Docker Engine、Docker Compose 插件和 Git。创建服务器专用配置文件；
配置项参考仓库中的 `.env.example`：

```bash
sudo install -d -m 750 -o root -g docker /opt/cordelia
sudoedit /opt/cordelia/.env
sudo chown root:docker /opt/cordelia/.env
sudo chmod 640 /opt/cordelia/.env
```

打开仓库 `discodyer/Cordelia` 的 **Settings → Actions → Runners → New
self-hosted runner**。在服务器上用专门的普通用户执行页面给出的下载和配置命令，
配置 runner 时给 `./config.sh` 命令添加 `--labels cordelia`。随后在 runner
目录执行 `sudo ./svc.sh install` 和 `sudo ./svc.sh start`，让它开机自启。

runner 用户必须能调用 Docker，并能读取上面的 `.env`：

```bash
sudo usermod -aG docker ACTIONS_RUNNER_USER
# 在 runner 目录执行，使新增用户组对服务生效：
sudo ./svc.sh stop
sudo ./svc.sh start
```

将 `ACTIONS_RUNNER_USER` 替换成实际用户。确保 GitHub 页面上的 runner 状态为
**Idle**，然后推送 `main` 或在 **Actions → Deploy Cordelia → Run workflow**
手动部署一次。

在 GitHub 的 **Actions** 页面查看构建结果。服务器上可用以下命令查看容器：

```bash
docker ps --filter name=cordelia
docker logs -f cordelia-cordelia-1
```

生产密钥只放在 `/opt/cordelia/.env`，它不会进入仓库或镜像。runner 应仅注册到
这个仓库，并保持更新；Docker 用户组拥有宿主机的高权限，请勿让不受信任的代码
获得向 `main` 推送的权限。

修改 `.env` 后，在 Actions 页面重新运行部署以应用配置。手动部署时，在 checkout
目录执行以下命令；`restart` 不会应用新的环境变量或挂载配置：

```bash
sudo env CORDELIA_ENV_FILE=/opt/cordelia/.env \
  docker compose up -d --build --force-recreate
```

正常连接 Telegram 后，日志会出现 `Delete old webhook`、`Start poll`。容器显示
运行中仅代表进程启动，请私聊机器人发送 `/ping` 验证消息收发。

## Documentation

See [Docs](https://nonebot.dev/)

## Commands

- `/ping` - Reply with pong
