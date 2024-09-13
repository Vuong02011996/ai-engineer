module.exports = {
  apps: [
    {
      name: "camera-ai",
      script: "source .venv/bin/activate && python main.py",
      args: [],
      exec_mode: "fork",
      instances: 1,
      wait_ready: true,
      autorestart: false,
      max_restarts: 5,
      interpreter: "",
      cron_restart: "",
      no_autorestart: true
    }
  ]
};
