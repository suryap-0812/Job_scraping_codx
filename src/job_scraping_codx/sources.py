from .models import Source


def default_sources() -> list[Source]:
    return [
        Source("RemoteOK Developer", "https://remoteok.com/remote-dev-jobs", "job_board", 180),
        Source("WeWorkRemotely Programming", "https://weworkremotely.com/categories/remote-programming-jobs", "job_board", 180),
        Source("AngelList Jobs", "https://wellfound.com/jobs", "job_board", 360),
        Source("Devpost Hackathons", "https://devpost.com/hackathons", "hackathon_platform", 180),
        Source("MLH Hackathons", "https://mlh.io/seasons/2025/events", "hackathon_platform", 360),
    ]
