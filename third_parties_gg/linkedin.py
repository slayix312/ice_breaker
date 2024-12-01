import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile
    """
    if mock:
        response = requests.get(
            "https://gist.githubusercontent.com/slayix312/e5d94bea84b00cbbb5b60594160c8094/raw/f3062e29a350b9b71c56a567ed7c7f446aee4699/gg.json"
        )
        response.raise_for_status()
        return response.json()

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"}
        response = requests.get(
            api_endpoint,
            headers=header_dic,
            params={"url": linkedin_profile_url},
            timeout=10,
        )

        data = response.json()
        data = {
            k: v
            for (k, v) in data.items()
            if v not in (None, [])
            and k not in ["people_also_viewed", "certifications"]
        }   
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")

        return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/guillermo-gaytan-a955169a/",
            mock=False,
        )
    )
