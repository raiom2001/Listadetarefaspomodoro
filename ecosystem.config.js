module.exports = {
  apps: [{
    name: 'organize-se',
    script: 'app.py',
    interpreter: 'python',
    env: {
      FLASK_ENV: 'production'
    }
  }]
}
