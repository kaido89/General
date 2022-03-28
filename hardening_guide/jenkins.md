# Add Cookie expiration date
sed -i 's_<!-- See https://www.owasp.org/index.php/HttpOnly for the discussion of this topic in OWASP -->_<max-age>3600</max-age>_g' /var/jenkins_cache/war/WEB-INF/web.xml;
