// rules.js

// This function is exported for use in the background script.
// It contains all the detection patterns for sensitive data.
function getDetectionRules() {
    return [
        // === Secrets & Credentials ===
        {
            name: 'Generic API Key',
            pattern: /\b(api_key|apikey|api-key|client_secret|api_token)\s*[:=]\s*['"]?[a-zA-Z0-9\-_]{20,}/i,
            description: 'A pattern resembling a generic API key or client secret was found.'
        },
        {
            name: 'High Entropy String',
            pattern: /(?=(?:.*[A-Z]))(?=(?:.*[a-z]))(?=(?:.*[0-9])_?)[A-Za-z0-9+/=]{40,}/,
            description: 'A long, high-entropy string was detected, which could be a private key or token.'
        },
        {
            name: 'AWS Access Key ID',
            pattern: /\b(AKIA|ASIA)[0-9A-Z]{16}\b/,
            description: 'An AWS Access Key ID was detected.'
        },
        {
            name: 'AWS Secret Access Key',
            pattern: /\b[A-Za-z0-9/+=]{40}\b/,
            description: 'A string resembling an AWS Secret Access Key was detected. Note: This may have false positives.'
        },
        {
            name: 'Google API Key',
            pattern: /\bAIza[0-9A-Za-z\-_]{35}\b/,
            description: 'A Google Cloud Platform API Key was detected.'
        },
        {
            name: 'GitHub Token',
            pattern: /\bghp_[a-zA-Z0-9]{36,}\b/,
            description: 'A GitHub Personal Access Token was detected.'
        },
        {
            name: 'Stripe API Key',
            pattern: /\b(sk|pk)_(test|live)_[0-9a-zA-Z]{24,}\b/,
            description: 'A Stripe API key was detected.'
        },
        {
            name: 'Private Key Block',
            pattern: /-----BEGIN ((RSA|OPENSSH|EC|PGP) )?PRIVATE KEY-----/i,
            description: 'A private key block (like RSA, OpenSSH, etc.) was found.'
        },

        // === Personally Identifiable Information (PII) ===
        {
            name: 'Email Address',
            pattern: /\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b/,
            description: 'An email address was found.'
        },
        {
            name: 'U.S. Social Security Number',
            pattern: /\b\d{3}-\d{2}-\d{4}\b/,
            description: 'A U.S. Social Security Number (SSN) was detected.'
        },
        {
            name: 'Credit Card Number',
            pattern: /\b(?:\d[ -]*?){13,16}\b/,
            description: 'A sequence of numbers resembling a credit card was found.'
        },
        {
            name: 'Phone Number',
            pattern: /\b(\(\d{3}\)|\d{3})[ -]?\d{3}[ -]?\d{4}\b/,
            description: 'A U.S. phone number format was detected.'
        },
        
        // === Confidentiality & Intellectual Property Keywords ===
        {
            name: 'Confidentiality Keyword',
            pattern: /\b(confidential|proprietary|internal use only|attorney-client privilege|secret|not for distribution)\b/i,
            description: 'A keyword indicating confidentiality was found.'
        },
        {
            name: 'Financial Keyword',
            pattern: /\b(salary|revenue|ebitda|forecast|m&a|acquisition|ipo)\b/i,
            description: 'A keyword related to sensitive financial information was detected.'
        },
        {
            name: 'Source Code Keyword',
            pattern: /\b(copyright|license|proprietary code|trade secret)\b/i,
            description: 'A keyword related to proprietary source code was detected.'
        },
        {
            name: 'Security Keyword',
            pattern: /\b(password|credential|network diagram|vulnerability|exploit|zeroday)\b/i,
            description: 'A keyword related to sensitive security information was detected.'
        }
    ];
}
