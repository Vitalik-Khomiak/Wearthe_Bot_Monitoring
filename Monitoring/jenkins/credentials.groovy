import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.impl.*
import com.cloudbees.plugins.credentials.*
import jenkins.model.*
import hudson.util.Secret

// Функція для отримання змінних середовища
def getEnvVariable(String name) {
    return System.getenv(name)
}

def dockerUserName = getEnvVariable('DOCKERHUB_USERNAME')
def dockerPassword = getEnvVariable('DOCKERHUB_PASSWORD')

def tgBotToken = getEnvVariable('TG_BOT_TOKEN')
def openaiApiKey = getEnvVariable('OPENAI_API_KEY')
def openWeatherToken = getEnvVariable('OPEN_WEATHER_TOKEN')

def domain = Domain.global()
def store = Jenkins.instance.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()
def creds = new UsernamePasswordCredentialsImpl(CredentialsScope.GLOBAL, "dockerhub_token", "Description", dockerUserName, dockerPassword)

store.addCredentials(domain, creds)

def tgBotTokenCreds = new StringCredentialsImpl(CredentialsScope.GLOBAL, "tg_bot_token", "TG Bot Token", tgBotToken)
store.addCredentials(domain, tgBotTokenCreds)
def openaiApiKeyCreds = new StringCredentialsImpl(CredentialsScope.GLOBAL, "openai_api_key", "OpenAI API Key", openaiApiKey)
store.addCredentials(domain, openaiApiKeyCreds)
def openWeatherTokenCreds = new StringCredentialsImpl(CredentialsScope.GLOBAL, "open_weather_token", "Open Weather Token", openWeatherToken)
store.addCredentials(domain, openWeatherTokenCreds)