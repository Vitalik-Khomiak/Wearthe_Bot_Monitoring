import jenkins.model.*

def instance = Jenkins.getInstance()
def job = instance.getItem('Weather_art_bot')

if (job) {
    println("Triggering job: ${job.name}")
    instance.queue.schedule(job, 0)
} else {
    println("Job not found: triggeredJob")
}