import re
from pathlib import Path

DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / 'templates' / 'static' / 'models' / 'job_description.txt'

SKILL_ALIASES = {
    'python': 'python',
    'py': 'python',
    'flask': 'flask',
    'django': 'django',
    'fastapi': 'fastapi',
    'sql': 'sql',
    'sql server': 'sql',
    'postgres': 'postgresql',
    'postgresql': 'postgresql',
    'mysql': 'mysql',
    'sqlite': 'sqlite',
    'mongodb': 'mongodb',
    'mongo': 'mongodb',
    'aws': 'aws',
    'amazon web services': 'aws',
    'azure': 'azure',
    'gcp': 'gcp',
    'google cloud': 'gcp',
    'docker': 'docker',
    'docker-compose': 'docker',
    'kubernetes': 'kubernetes',
    'k8s': 'kubernetes',
    'git': 'git',
    'github': 'github',
    'gitlab': 'gitlab',
    'rest api': 'rest api',
    'api': 'api',
    'json': 'json',
    'html': 'html',
    'css': 'css',
    'javascript': 'javascript',
    'js': 'javascript',
    'react': 'react',
    'reactjs': 'react',
    'angular': 'angular',
    'vue': 'vue',
    'node': 'node',
    'node.js': 'node',
    'nodejs': 'node',
    'express': 'express',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'scikit-learn': 'scikit-learn',
    'machine learning': 'machine learning',
    'ml': 'machine learning',
    'data visualization': 'data visualization',
    'data viz': 'data visualization',
    'data analysis': 'data analysis',
    'business intelligence': 'business intelligence',
    'ci/cd': 'ci/cd',
    'jenkins': 'ci/cd',
    'github actions': 'ci/cd',
    'circleci': 'ci/cd',
    'tensorflow': 'tensorflow',
    'pytorch': 'pytorch',
    'linux': 'linux',
    'bash': 'bash',
    'powershell': 'powershell',
    'power bi': 'power bi',
    'powerbi': 'power bi',
    'excel': 'excel',
    'tableau': 'tableau',
    'jira': 'jira',
    'agile': 'agile',
    'scrum': 'scrum',
    'spark': 'spark',
    'redis': 'redis',
    'kafka': 'kafka',
    'hadoop': 'hadoop',
    'spring': 'spring',
    'spring boot': 'spring',
    'microservices': 'microservices',
    'cloud': 'cloud',
    'aws cloud': 'cloud',
    'google cloud platform': 'gcp',
    'gcp': 'gcp',
    'c++': 'c++',
    'cpp': 'c++',
    'c#': 'c#',
    '.net': '.net',
    'dotnet': '.net',
    'java': 'java',
    'scala': 'scala',
    'php': 'php',
    'ruby': 'ruby',
    'communication': 'communication',
    'presentation': 'communication',
    'teamwork': 'communication',
    'leadership': 'communication',
    'aws lambda': 'aws',
    'serverless': 'aws'
}

def load_job_description():
    if not DEFAULT_MODEL_PATH.exists():
        return ''
    return DEFAULT_MODEL_PATH.read_text(encoding='utf-8')


def extract_job_title(text):
    if not text:
        return ''

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    first_line = lines[0] if lines else text
    first_line = re.sub(r'^(we are looking for|looking for|seeking|required|job opening for|we need a|we need an)\b[:, ]*', '', first_line, flags=re.I)
    first_line = re.split(r'\bwith\b|\bfor\b|\bwho\b|\bthat\b|\bto\b', first_line, flags=re.I)[0].strip()
    return first_line


ROLE_STOPWORDS = {
    'and', 'or', 'with', 'the', 'for', 'a', 'an', 'to', 'of', 'in', 'on', 'at', 'by', 'from',
    'senior', 'junior', 'lead', 'manager', 'engineer', 'developer', 'specialist', 'expert',
    'analyst', 'scientist', 'candidate', 'professional', 'focused', 'looking', 'seeking',
    'experience', 'skills', 'skill', 'role', 'position', 'responsibilities', 'job'
}


def extract_role_keywords(title):
    if not title:
        return []
    words = normalize_text(title).split()
    return [word for word in words if word not in ROLE_STOPWORDS and len(word) > 2]


def calculate_role_match(resume_text, keywords):
    if not keywords:
        return None
    normalized_resume = normalize_text(resume_text)
    if not normalized_resume:
        return 0.0
    hits = sum(1 for keyword in keywords if re.search(r'\b' + re.escape(keyword) + r'\b', normalized_resume))
    return round(hits / len(keywords) * 100, 2)


def normalize_text(text):
    if not text:
        return ''
    cleaned = text.lower()
    cleaned = cleaned.replace('-', ' ').replace('/', ' ').replace('.', ' ')
    cleaned = re.sub(r'[\u2013\u2014\u2015]+', ' ', cleaned)
    cleaned = re.sub(r'[^\w+#]+', ' ', cleaned)
    return re.sub(r'\s+', ' ', cleaned).strip()


def extract_skills(text):
    if not text:
        return set()

    normalized = normalize_text(text)
    skills = set()
    ordered_aliases = sorted(SKILL_ALIASES.items(), key=lambda item: -len(item[0]))

    for variant, canonical in ordered_aliases:
        pattern = r'\b' + re.escape(variant) + r'\b'
        if re.search(pattern, normalized):
            skills.add(canonical)

    return skills


def extract_years_of_experience(text):
    if not text:
        return 'Not found'

    range_match = re.search(r'(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(?:years|yrs)\b', text, flags=re.IGNORECASE)
    if range_match:
        start, end = map(float, range_match.groups())
        if start.is_integer() and end.is_integer():
            return f'{int(start)}-{int(end)} years'
        return f'{start}-{end} years'

    years_match = re.search(r'(\d+(?:\.\d+)?)(?:\+)?\s*(?:years|yrs)\b', text, flags=re.IGNORECASE)
    if years_match:
        years = float(years_match.group(1))
        return f'{int(years)} years' if years.is_integer() else f'{years} years'

    return 'Not found'


def extract_education(text):
    if not text:
        return 'Not found'

    degree_patterns = [
        'phd', 'ph.d.', 'doctor of philosophy',
        'm.s.', 'ms', 'master of science', 'm.a.', 'ma', 'master of arts', 'mba',
        'b.s.', 'bs', 'bachelor of science', 'b.a.', 'ba', 'bachelor of arts',
        'associate', 'diploma', 'high school'
    ]

    for degree in degree_patterns:
        if re.search(r'\b' + re.escape(degree) + r'\b', text, flags=re.IGNORECASE):
            return degree.upper() if degree.isupper() else degree.title()

    return 'Not found'


def extract_contact(text):
    if not text:
        return 'Not found'

    email_match = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
    phone_match = re.search(r'(?:\+\d{1,3}[\s-]?)?(?:\(\d{2,4}\)|\d{2,4})[\s-]?\d{3,4}[\s-]?\d{3,4}', text)

    if email_match:
        return email_match.group(0)
    if phone_match:
        return phone_match.group(0)

    return 'Not found'


def generate_resume_summary(text):
    return {
        'experience': extract_years_of_experience(text),
        'education': extract_education(text),
        'contact': extract_contact(text),
    }


def analyze_resume(text, job_desc_text=None):
    resume_text = text or ''
    jd_text = job_desc_text.strip() if job_desc_text and job_desc_text.strip() else load_job_description()

    job_title = extract_job_title(jd_text)
    role_keywords = extract_role_keywords(job_title)
    role_match_percent = calculate_role_match(resume_text, role_keywords)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    skill_match_percent = round(len(matched) / len(jd_skills) * 100, 2) if jd_skills else None
    match_percent = skill_match_percent

    if skill_match_percent is None:
        overall_score = role_match_percent
    elif role_match_percent is None:
        overall_score = skill_match_percent
    else:
        overall_score = round(skill_match_percent * 0.7 + role_match_percent * 0.3, 2)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_match_percent": skill_match_percent,
        "match_percent": match_percent,
        "role_match_percent": role_match_percent,
        "overall_score": overall_score,
        "job_title": job_title,
        "resume_skills": sorted(resume_skills),
        "job_description_skills": sorted(jd_skills),
        "resume_summary": generate_resume_summary(resume_text),
    }