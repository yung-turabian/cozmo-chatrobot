from bardapi import BardCookies

COOKIE_DICT = {
    "__Secure-1PSID": "cgiriqXG5Q4KK-ug-lutcSWfY3syECXEU_Fb7l6Cp61utKabLQ1QIBdRZyeM4CUWgYv6LQ.",
    "__Secure-1PSIDTS": "sidts-CjEBNiGH7iDSo9t0DzNZnHCR93C67WSonEUdPY4O5T1pZ9GFMeADRVPircsf9qlWvZtFEAA",
    "__Secure-1PSIDCC": "ACA-OxO9kstfQSZ1-M0G52DvUGDkC_Vjos8y__OsLEmyDi7RosteAjJowVUvtXKrlizftdstw9U",
}

bard = BardCookies(cookie_dict=COOKIE_DICT)
audio = bard.speech('the branch of astronomy concerned with the physical nature of stars and other celestial bodies, and the application of the laws and theories of physics to the interpretation of astronomical observations.')
with open("speech.ogg", "wb") as f:
  f.write(bytes(audio['audio']))
#print(bard.get_answer("Can")['content'])