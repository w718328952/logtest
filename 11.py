import re

out_s = 'FB Cnt:33 | Width:2004 FB ping;fre=146000,duty=500,vol=0,VpA=5040,type=1,coil=1 sipa 70mA c'

# 提取VPA和IPA值
matchObj1 = re.compile(r'((vpa=)+(\d+)+)', re.I | re.S)
matchObj2 = re.compile(r'((ipa=)+(\d+)+)', re.I | re.S)
result = matchObj1.match("vpa")
print(matchObj1)
# 将VPA和IPA值存入列表中
vpa_cont = matchObj1.findall(out_s)
ipa_cont = matchObj2.findall(out_s)
print(vpa_cont)
print(ipa_cont)