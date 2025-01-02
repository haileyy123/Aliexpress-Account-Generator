import seleniumwire.undetected_chromedriver as uc

def start_chrome_driver(options=uc.ChromeOptions(), proxy=None, proxyport=None, username=None, password=None):
    if proxy is not None:
        proxy_address = f"http://{username}:{password}@{proxy}:{proxyport}"

        proxy_options = {
            "proxy": {
                "http": proxy_address,
                "https": proxy_address,
            }
        }
        
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
            
        driver = uc.Chrome(
            seleniumwire_options=proxy_options,
            options = options,
            use_subprocess=False,
        )

        return driver
    else:
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
            
        driver = uc.Chrome(
            options = options,
            use_subprocess=False,
        )
        return driver