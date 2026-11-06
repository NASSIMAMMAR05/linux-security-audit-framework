#!/usr/bin/env python3
"""
Module 4: Scoring sécurité basé sur CVSS
Classification: Low / Medium / High / Critical
"""

def calculate_severity_score(findings, cve_results=None):
    """Calculate security score based on findings and CVEs"""
    
    severity_weights = {
        'CRITICAL': 25,
        'HIGH': 15,
        'MEDIUM': 8,
        'LOW': 3
    }
    
    total_penalty = 0
    max_score = 100
    
    # Penalty from findings
    for finding in findings:
        severity = finding.get('severity', 'LOW')
        total_penalty += severity_weights.get(severity, 3)
    
    # Penalty from CVEs
    if cve_results:
        cve_count = len(cve_results)
        if cve_count > 0:
            # Each CVE package adds penalty
            cve_penalty = min(cve_count * 5, 30)  # Max 30 points penalty from CVEs
            total_penalty += cve_penalty
    
    score = max(0, max_score - total_penalty)
    
    # Determine grade
    if score >= 90:
        grade = "A+ (Excellent - Very Secure)"
        status = "🟢"
    elif score >= 80:
        grade = "A (Good - Minor Issues)"
        status = "🟢"
    elif score >= 70:
        grade = "B (Average - Needs Improvement)"
        status = "🟡"
    elif score >= 60:
        grade = "C (Below Average - Security Gaps)"
        status = "🟡"
    elif score >= 50:
        grade = "D (Poor - Critical Issues)"
        status = "🔴"
    else:
        grade = "F (Very Poor - Urgent Action Required)"
        status = "🔴"
    
    return {
        'score': score,
        'grade': grade,
        'status': status,
        'penalty': total_penalty,
        'max_score': max_score
    }

def get_recommendations(findings, cve_results=None):
    """Generate remediation recommendations"""
    recommendations = []
    
    for finding in findings:
        if 'fix' in finding:
            recommendations.append({
                'issue': finding['title'],
                'fix': finding['fix'],
                'severity': finding['severity']
            })
    
    if cve_results:
        for cve in cve_results:
            recommendations.append({
                'issue': f"CVE: {cve.get('package', 'Unknown')} ({cve.get('count', 0)} vulnerabilities)",
                'fix': f"sudo apt update && sudo apt install --only-upgrade {cve.get('package', '')} -y",
                'severity': 'HIGH'
            })
    
    return recommendations

if __name__ == "__main__":
    test_findings = [
        {'severity': 'HIGH', 'title': 'Test finding'},
        {'severity': 'MEDIUM', 'title': 'Another finding'}
    ]
    test_cves = [{'package': 'test', 'count': 5}]
    result = calculate_severity_score(test_findings, test_cves)
    print(f"Score: {result['score']}/100")
    print(f"Grade: {result['grade']}")
