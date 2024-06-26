#!/usr/bin/python
#https://github.com/Ar30t/attcknav_empire
import sys
import os
import argparse
import csv
import time
import gen_layer
import fnmatch

# Find agent.log files
def files_within(directory_path, pattern="agent.log"):
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for file_name in fnmatch.filter(filenames, pattern):
            yield os.path.join(dirpath, file_name)

def main():
    techniques = {
    "Invoke-Mimikatz memssp":  ["T1101"],
    "Invoke-Mimikatz SkeletonKey":  ["T1098"],
    "Add-NetUser":  ["T1033"],
    "Get-SecurityPackages":  ["T1101"],
    "Invoke-Mimikatz Add-SIDHistory":  ["T1178"],
    "Invoke-AccessBinary":  ["T1044"],
    "Invoke-DisableMachineAcctChange":  ["T1098"],
    "Install-SSP":  ["T1101"],
    "Invoke-WMI":  ["T1047"],
    "Invoke-RIDHijacking":  ["T1003"],
    "Invoke-Schtasks":  ["T1053"],
    "Invoke-Registry":  ["T1060"],
    "Invoke-WMI":  ["T1084"],
    "Invoke-BackdoorLNK":  ["T1204", "T1023"],
    "Invoke-Schtasks":  ["T1053"],
    "Invoke-Registry":  ["T1060"],
    "Invoke-DeadUserBackdoor":  ["T1098"],
    "Invoke-ResolverBackdoor":  ["T1015"],
    "Invoke-EventLogBackdoor":  ["T1084"],
    "Invoke-BypassUAC":  ["T1088"],
    "Invoke-Ask":  ["T1088"],
    "Invoke-Watson":  ["T1068"],
    "PrintNightmare":  ["T1068"],
    "Invoke-BypassUACTokenManipulation":  ["T1088"],
    "Invoke-SDCLTBypass":  ["T1088"],
    "Invoke-EnvBypass":  ["T1088"],
    "Invoke-MS16032":  ["T1068"],
    "Invoke-Tater":  ["T1187"],
    "Get Group Policy Preferences":  ["T1548"],
    "Invoke-WScriptBypassUAC":  ["T1088"],
    "Invoke-EventVwrBypass":  ["T1088"],
    "Sherlock":  ["T1046"],
    "PrivescCheck":  ["T1046"],
    "Sweet Potato Local Service to SYSTEM Privilege Escalation":  ["T1068"],
    "Invoke-FodHelperBypass":  ["T1088"],
    "Get-GPPPassword":  ["T1003"],
    "Get-SiteListPassword":  ["T1003"],
    "Get Group Policy Preferences":  ["T1038"],
    "Invoke-winPEAS":  ["T1046"],
    "Invoke-MS16135":  ["T1068"],
    "Get-System":  ["T1103"],
    "Install-ServiceBinary":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Invoke-AllChecks":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Install-ServiceBinary":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Write-HijackDll":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Invoke-ServiceAbuse":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Restore-ServiceBinary":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Find-ProcessDLLHijack":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Invoke-ServiceAbuse":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Exploit-JBoss":  ["T1210"],
    "Exploit-Jenkins":  ["T1210"],
    "Invoke-EternalBlue":  ["T1210"],
    "Invoke-SpoolSample":  ["T1547"],
    "Invoke-EgressCheck":  ["T1041"],
    "Invoke-DropboxUpload":  ["T1041"],
    "Start-MonitorTCPConnections":  ["T1049"],
    "Get-AntiVirusProduct":  ["T1063"],
    "Invoke-WinEnum":  ["T1082"],
    "Get-ComputerDetails":  ["T1082"],
    "Get-Proxy":  ["T1049"],
    "Get-PathAcl":  ["T1083"],
    "Get-SystemDNSServer":  ["T1482", "T1018"],
    "Get-UACLevel":  ["T1033"],
    "Find-TrustedDocuments":  ["T1135"],
    "Get-AppLockerConfig":  ["T1012"],
    "Invoke-Paranoia":  ["T1057"],
    "Invoke-HostRecon":  ["T1082"],
    "Invoke-Seatbelt":  ["T1082"],
    "Get-SPN":  ["T1207"],
    "Invoke-Portscan":  ["T1046"],
    "Invoke-BloodHound":  ["T1484"],
    "Invoke-ReverseDNSLookup":  ["T1046"],
    "Get-SQLInstanceDomain":  ["T1046"],
    "Invoke-SMBScanner":  ["T1135", "T1187"],
    "Get-SQLServerInfo":  ["T1046"],
    "Invoke-SMBAutoBrute":  ["T1135", "T1187"],
    "Invoke-ARPScan":  ["T1016"],
    "Get-KerberosServiceTicket":  ["T1097"],
    "Invoke-BloodHound":  ["T1484"],
    "Invoke-SMBLogin":  ["T1135", "T1187"],
    "Get-ADIDNSPermission":  ["T1069"],
    "Get-ADIDNSZone":  ["T1016"],
    "Get-DomainDFSshare":  ["T1420"],
    "Get-DomainUser":  ["T1033"],
    "Get-NetLocalGroup":  ["T1482"],
    "Get-DomainSubnet":  ["T1016"],
    "Get-NetSession":  ["T1482"],
    "Set-DomainObject":  ["T1487"],
    "Get-DomainGPOUserLocalGroupMapping":  ["T1069"],
    "Get-DomainComputer":  ["T1082"],
    "Get-Forest":  ["T1482"],
    "Get-DomainManagedSecurityGroup":  ["T1069"],
    "Get-DomainTrust":  ["T1482"],
    "Get-DomainGPO":  ["T1484"],
    "Get-DomainForeignUser":  ["T1482"],
    "Get-NetRDPSession":  ["T1076"],
    "Get-GPOComputer":  ["T1484"],
    "Get-WMIRegCachedRDPConnection":  ["T1076"],
    "Get-DomainGPOComputerLocalGroupMapping":  ["T1069"],
    "Get-DomainSite":  ["T1482"],
    "Get-ForestDomain":  ["T1482"],
    "Get-DomainPolicyData":  ["T1482"],
    "Get-DomainTrustMapping":  ["T1482"],
    "Get-DomainFileServer":  ["T1083"],
    "Get-DomainController":  ["T1482"],
    "Find-LocalAdminAccess":  ["T1069"],
    "Get-DomainForeignGroupMember":  ["T1482"],
    "Get-SubnetRanges":  ["T1016"],
    "Get-DomainGroup":  ["T1482"],
    "Find-DomainUserLocation":  ["T1033"],
    "Find-DomainProcess":  ["T1057"],
    "Get-DomainOU":  ["T1482"],
    "Get-DomainObjectAcl":  ["T1003"],
    "Get-DomainGroupMember":  ["T1482"],
    "Get-NetLoggedon":  ["1134"],
    "Find-DomainShare":  ["T1135"],
    "Invoke-ShellcodeMSIL":  ["T1064"],
    "Invoke-ReflectivePEInjection":  ["T1055"],
    "Invoke-Shellcode":  ["T1064"],
    "Invoke-Boolang":  ["T1059"],
    "Invoke-Ntsd":  ["T1127"],
    "Invoke-SSharp":  ["T1059"],
    "Invoke-DllInjection":  ["T1055"],
    "Invoke-IronPython":  ["T1059"],
    "Invoke-MetasploitPayload":  ["T1055"],
    "Invoke-ClearScript":  ["T1059"],
    "Invoke-Assembly":  ["T1059"],
    "Invoke-SessionGopher":  ["T1081"],
    "Invoke-PowerDump":  ["T1003"],
    "Get-VaultCredential":  ["T1503"],
    "DomainPasswordSpray":  ["T1110"],
    "Invoke-Kerberoast":  ["T1208"],
    "Invoke-SharpSecDump":  ["T1003"],
    "Invoke-TokenManipulation":  ["T1134"],
    "enum_cred_store":  ["T1003"],
    "Invoke-Rubeus":  ["T1208", "T1097"],
    "Invoke-NTLMExtract":  ["T1003"],
    "Get-LAPSPasswords":  ["T1003"],
    "Invoke-InternalMonologue":  ["T1003"],
    "Invoke-CredentialInjection":  ["T1214", "T1003"],
    "Invoke-Mimikatz DumpCreds":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Dump Terminal Server Passwords":  ["T1003", "T1081"],
    "Invoke-Mimikatz DCsync":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz DumpKeys":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz LSA Dump":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Silver Ticket":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz LSA Dump":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz DumpCerts":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Golden Ticket":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Golden Ticket":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz DCsync - Full Hashdump":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz SAM dump":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz PTH":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz extract kerberos tickets.":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz TrustKeys":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Tokens":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Command":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-SQLOSCMD":  ["T1505"],
    "Invoke-WMI":  ["T1047"],
    "Invoke-PortFwd":  ["T1363"],
    "New-GPOImmediateTask":  ["T1053"],
    "Invoke-DCOM":  ["T1175"],
    "Exploit-Jenkins":  ["T1210"],
    "Invoke-SSHCommand":  ["T1071"],
    "Invoke-InveighRelay":  ["T1171"],
    "Invoke-PSRemoting":  ["T1028"],
    "Invoke-WMIDebugger":  ["T1047"],
    "Invoke-ExecuteMSBuild":  ["T1127", "T1047"],
    "Invoke-SMBExec":  ["T1187", "T1135", "T1047"],
    "Invoke-PsExec":  ["T1035", "T1077"],
    "Set-Wallpaper":  ["T1491"],
    "Invoke-VoiceTroll":  ["T1491"],
    "Invoke-RickASCII":  ["T1491"],
    "Invoke-Message":  ["T1491"],
    "Invoke-WLMDR":  ["T1491"],
    "Get-RickAstley":  ["T1491"],
    "Get-Schwifty":  ["T1491"],
    "Invoke-Thunderstruck":  ["T1491"],
    "Invoke-ProcessKiller":  ["T1491"],
    "Invoke-SocksProxy":  ["T1090"],
    "Switch-Listener":  ["T1008"],
    "Invoke-Mimikatz Multirdp":  ["T1076"],
    "Invoke-Vnc":  ["T1021"],
    "Invoke-SharpChiselClient":  ["T1090"],
    "Invoke-PSInject":  ["T1055"],
    "Get-DomainSID":  ["T1178"],
    "Start-ProcessAsUser":  ["T1088"],
    "Invoke-Script":  ["T1064"],
    "Invoke-Phant0m":  ["T1070", "T1089"],
    "Invoke-LockWorkStation":  ["T1098"],
    "User-to-SID":  ["T1098"],
    "Invoke-RunAs":  ["T1088"],
    "Enable-RDP":  ["T1076"],
    "Invoke-ZipFolder":  ["T1002"],
    "Spawn":  ["T1055"],
    "PowerCat":  ["T1036"],
    "Shinject":  ["T1055"],
    "Invoke-WdigestDowngrade":  ["T1214"],
    "New-HoneyHash":  ["T1177"],
    "Invoke-PSInject":  ["T1055"],
    "Restart-Computer":  ["T1064"],
    "SID-to-User":  ["T1098"],
    "Invoke-SpawnAs":  ["T1055"],
    "Disable-RDP":  ["T1076"],
    "Logoff User":  ["T1098"],
    "Invoke-DowngradeAccount":  ["T1098"],
    "Timestomp":  ["T1099"],
    "Invoke-SendMail":  ["T1114"],
    "Disable-SecuritySettings":  ["T1047"],
    "View-Email":  ["T1114"],
    "Get-SubFolders":  ["T1114"],
    "Invoke-MailSearch":  ["T1114"],
    "Get-EmailItems":  ["T1114"],
    "Invoke-SearchGAL":  ["T1114"],
    "Fetch local accounts on a member server and perform an online brute force attack":  ["T1110"],
    "HTTP-Login":  ["T1071"],
    "Get-SQLServerLoginDefaultPw":  ["T1256"],
    "Find-Fruit":  ["T1102", "T1256"],
    "Invoke-CredentialPhisher":  ["T1141", "T1514"],
    "Invoke-SauronEye":  ["T1083"],
    "Get-Screenshot":  ["T1113"],
    "Get Microsoft Updates":  ["T1082"],
    "Invoke-NinjaCopy":  ["T1105"],
    "Start-WebcamRecorder":  ["T1125"],
    "Invoke-PacketCapture":  ["T1040"],
    "Invoke-SharpLoginPrompt":  ["T1056"],
    "Out-Minidump":  ["T1033"],
    "Invoke-Inveigh":  ["T1171"],
    "Invoke-NetRipper":  ["T1179", "T1410"],
    "Invoke-WireTap":  ["T1123", "T1125", "T1056"],
    "Find-InterestingFile":  ["T1083"],
    "Get-USBKeyStrokes":  ["T1056"],
    "Get-BrowserData":  ["T1503"],
    "Get-SQLQuery":  ["T1046"],
    "Invoke-FileFinder":  ["T1083"],
    "Get-ChromeDump":  ["T1503"],
    "Get-SQLColumnSampleData":  ["T1046"],
    "Get-IndexedItem":  ["T1083"],
    "Get-KeyStrokes":  ["T1056"],
    "FoxDump":  ["T1503"],
    "Invoke-EventVwrBypass":  ["T1141", "T1514"],
    "Get-ClipboardContents":  ["T1115", "T1414"],
    "Get-SharpChromium":  ["T1503"],
    "Get-KeePassconfig":  ["T1119"],
    "Add-KeePassConfigTrigger":  ["T1119"],
    "Invoke-KeeThief":  ["T1033"],
    "Remove-KeePassConfigTrigger":  ["T1033"],
    "Find-KeePassconfig":  ["T1119"],
    "Invoke-Mimikatz memssp":  ["T1101"],
    "Invoke-Mimikatz SkeletonKey":  ["T1098"],
    "Add-NetUser":  ["T1033"],
    "Get-SecurityPackages":  ["T1101"],
    "Invoke-Mimikatz Add-SIDHistory":  ["T1178"],
    "Invoke-AccessBinary":  ["T1044"],
    "Invoke-DisableMachineAcctChange":  ["T1098"],
    "Install-SSP":  ["T1101"],
    "Invoke-WMI":  ["T1047"],
    "Invoke-RIDHijacking":  ["T1003"],
    "Invoke-Schtasks":  ["T1053"],
    "Invoke-Registry":  ["T1060"],
    "Invoke-WMI":  ["T1084"],
    "Invoke-BackdoorLNK":  ["T1204", "T1023"],
    "Invoke-Schtasks":  ["T1053"],
    "Invoke-Registry":  ["T1060"],
    "Invoke-DeadUserBackdoor":  ["T1098"],
    "Invoke-ResolverBackdoor":  ["T1015"],
    "Invoke-EventLogBackdoor":  ["T1084"],
    "Invoke-BypassUAC":  ["T1088"],
    "Invoke-Ask":  ["T1088"],
    "Invoke-Watson":  ["T1068"],
    "PrintNightmare":  ["T1068"],
    "Invoke-BypassUACTokenManipulation":  ["T1088"],
    "Invoke-SDCLTBypass":  ["T1088"],
    "Invoke-EnvBypass":  ["T1088"],
    "Invoke-MS16032":  ["T1068"],
    "Invoke-Tater":  ["T1187"],
    "Get Group Policy Preferences":  ["T1548"],
    "Invoke-WScriptBypassUAC":  ["T1088"],
    "Invoke-EventVwrBypass":  ["T1088"],
    "Sherlock":  ["T1046"],
    "PrivescCheck":  ["T1046"],
    "Sweet Potato Local Service to SYSTEM Privilege Escalation":  ["T1068"],
    "Invoke-FodHelperBypass":  ["T1088"],
    "Get-GPPPassword":  ["T1003"],
    "Get-SiteListPassword":  ["T1003"],
    "Get Group Policy Preferences":  ["T1038"],
    "Invoke-winPEAS":  ["T1046"],
    "Invoke-MS16135":  ["T1068"],
    "Get-System":  ["T1103"],
    "Install-ServiceBinary":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Invoke-AllChecks":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Install-ServiceBinary":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Write-HijackDll":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Invoke-ServiceAbuse":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Restore-ServiceBinary":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Find-ProcessDLLHijack":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Invoke-ServiceAbuse":  ["T1087", "T1038", "T1031", "T1034", "T1057", "T1012"],
    "Exploit-JBoss":  ["T1210"],
    "Exploit-Jenkins":  ["T1210"],
    "Invoke-EternalBlue":  ["T1210"],
    "Invoke-SpoolSample":  ["T1547"],
    "Invoke-EgressCheck":  ["T1041"],
    "Invoke-DropboxUpload":  ["T1041"],
    "Start-MonitorTCPConnections":  ["T1049"],
    "Get-AntiVirusProduct":  ["T1063"],
    "Invoke-WinEnum":  ["T1082"],
    "Get-ComputerDetails":  ["T1082"],
    "Get-Proxy":  ["T1049"],
    "Get-PathAcl":  ["T1083"],
    "Get-SystemDNSServer":  ["T1482", "T1018"],
    "Get-UACLevel":  ["T1033"],
    "Find-TrustedDocuments":  ["T1135"],
    "Get-AppLockerConfig":  ["T1012"],
    "Invoke-Paranoia":  ["T1057"],
    "Invoke-HostRecon":  ["T1082"],
    "Invoke-Seatbelt":  ["T1082"],
    "Get-SPN":  ["T1207"],
    "Invoke-Portscan":  ["T1046"],
    "Invoke-BloodHound":  ["T1484"],
    "Invoke-ReverseDNSLookup":  ["T1046"],
    "Get-SQLInstanceDomain":  ["T1046"],
    "Invoke-SMBScanner":  ["T1135", "T1187"],
    "Get-SQLServerInfo":  ["T1046"],
    "Invoke-SMBAutoBrute":  ["T1135", "T1187"],
    "Invoke-ARPScan":  ["T1016"],
    "Get-KerberosServiceTicket":  ["T1097"],
    "Invoke-BloodHound":  ["T1484"],
    "Invoke-SMBLogin":  ["T1135", "T1187"],
    "Get-ADIDNSPermission":  ["T1069"],
    "Get-ADIDNSZone":  ["T1016"],
    "Get-DomainDFSshare":  ["T1420"],
    "Get-DomainUser":  ["T1033"],
    "Get-NetLocalGroup":  ["T1482"],
    "Get-DomainSubnet":  ["T1016"],
    "Get-NetSession":  ["T1482"],
    "Set-DomainObject":  ["T1487"],
    "Get-DomainGPOUserLocalGroupMapping":  ["T1069"],
    "Get-DomainComputer":  ["T1082"],
    "Get-Forest":  ["T1482"],
    "Get-DomainManagedSecurityGroup":  ["T1069"],
    "Get-DomainTrust":  ["T1482"],
    "Get-DomainGPO":  ["T1484"],
    "Get-DomainForeignUser":  ["T1482"],
    "Get-NetRDPSession":  ["T1076"],
    "Get-GPOComputer":  ["T1484"],
    "Get-WMIRegCachedRDPConnection":  ["T1076"],
    "Get-DomainGPOComputerLocalGroupMapping":  ["T1069"],
    "Get-DomainSite":  ["T1482"],
    "Get-ForestDomain":  ["T1482"],
    "Get-DomainPolicyData":  ["T1482"],
    "Get-DomainTrustMapping":  ["T1482"],
    "Get-DomainFileServer":  ["T1083"],
    "Get-DomainController":  ["T1482"],
    "Find-LocalAdminAccess":  ["T1069"],
    "Get-DomainForeignGroupMember":  ["T1482"],
    "Get-SubnetRanges":  ["T1016"],
    "Get-DomainGroup":  ["T1482"],
    "Find-DomainUserLocation":  ["T1033"],
    "Find-DomainProcess":  ["T1057"],
    "Get-DomainOU":  ["T1482"],
    "Get-DomainObjectAcl":  ["T1003"],
    "Get-DomainGroupMember":  ["T1482"],
    "Get-NetLoggedon":  ["1134"],
    "Find-DomainShare":  ["T1135"],
    "Invoke-ShellcodeMSIL":  ["T1064"],
    "Invoke-ReflectivePEInjection":  ["T1055"],
    "Invoke-Shellcode":  ["T1064"],
    "Invoke-Boolang":  ["T1059"],
    "Invoke-Ntsd":  ["T1127"],
    "Invoke-SSharp":  ["T1059"],
    "Invoke-DllInjection":  ["T1055"],
    "Invoke-IronPython":  ["T1059"],
    "Invoke-MetasploitPayload":  ["T1055"],
    "Invoke-ClearScript":  ["T1059"],
    "Invoke-Assembly":  ["T1059"],
    "Invoke-SessionGopher":  ["T1081"],
    "Invoke-PowerDump":  ["T1003"],
    "Get-VaultCredential":  ["T1503"],
    "DomainPasswordSpray":  ["T1110"],
    "Invoke-Kerberoast":  ["T1208"],
    "Invoke-SharpSecDump":  ["T1003"],
    "Invoke-TokenManipulation":  ["T1134"],
    "enum_cred_store":  ["T1003"],
    "Invoke-Rubeus":  ["T1208", "T1097"],
    "Invoke-NTLMExtract":  ["T1003"],
    "Get-LAPSPasswords":  ["T1003"],
    "Invoke-InternalMonologue":  ["T1003"],
    "Invoke-CredentialInjection":  ["T1214", "T1003"],
    "Invoke-Mimikatz DumpCreds":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Dump Terminal Server Passwords":  ["T1003", "T1081"],
    "Invoke-Mimikatz DCsync":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz DumpKeys":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz LSA Dump":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Silver Ticket":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz LSA Dump":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz DumpCerts":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Golden Ticket":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Golden Ticket":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz DCsync - Full Hashdump":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz SAM dump":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz PTH":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz extract kerberos tickets.":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz TrustKeys":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Tokens":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-Mimikatz Command":  ["T1098", "T1003", "T1081", "T1207", "T1075", "T1097", "T1145", "T1101", "T1178"],
    "Invoke-SQLOSCMD":  ["T1505"],
    "Invoke-WMI":  ["T1047"],
    "Invoke-PortFwd":  ["T1363"],
    "New-GPOImmediateTask":  ["T1053"],
    "Invoke-DCOM":  ["T1175"],
    "Exploit-Jenkins":  ["T1210"],
    "Invoke-SSHCommand":  ["T1071"],
    "Invoke-InveighRelay":  ["T1171"],
    "Invoke-PSRemoting":  ["T1028"],
    "Invoke-WMIDebugger":  ["T1047"],
    "Invoke-ExecuteMSBuild":  ["T1127", "T1047"],
    "Invoke-SMBExec":  ["T1187", "T1135", "T1047"],
    "Invoke-PsExec":  ["T1035", "T1077"],
    "Set-Wallpaper":  ["T1491"],
    "Invoke-VoiceTroll":  ["T1491"],
    "Invoke-RickASCII":  ["T1491"],
    "Invoke-Message":  ["T1491"],
    "Invoke-WLMDR":  ["T1491"],
    "Get-RickAstley":  ["T1491"],
    "Get-Schwifty":  ["T1491"],
    "Invoke-Thunderstruck":  ["T1491"],
    "Invoke-ProcessKiller":  ["T1491"],
    "Invoke-SocksProxy":  ["T1090"],
    "Switch-Listener":  ["T1008"],
    "Invoke-Mimikatz Multirdp":  ["T1076"],
    "Invoke-Vnc":  ["T1021"],
    "Invoke-SharpChiselClient":  ["T1090"],
    "Invoke-PSInject":  ["T1055"],
    "Get-DomainSID":  ["T1178"],
    "Start-ProcessAsUser":  ["T1088"],
    "Invoke-Script":  ["T1064"],
    "Invoke-Phant0m":  ["T1070", "T1089"],
    "Invoke-LockWorkStation":  ["T1098"],
    "User-to-SID":  ["T1098"],
    "Invoke-RunAs":  ["T1088"],
    "Enable-RDP":  ["T1076"],
    "Invoke-ZipFolder":  ["T1002"],
    "Spawn":  ["T1055"],
    "PowerCat":  ["T1036"],
    "Shinject":  ["T1055"],
    "Invoke-WdigestDowngrade":  ["T1214"],
    "New-HoneyHash":  ["T1177"],
    "Invoke-PSInject":  ["T1055"],
    "Restart-Computer":  ["T1064"],
    "SID-to-User":  ["T1098"],
    "Invoke-SpawnAs":  ["T1055"],
    "Disable-RDP":  ["T1076"],
    "Logoff User":  ["T1098"],
    "Invoke-DowngradeAccount":  ["T1098"],
    "Timestomp":  ["T1099"],
    "Invoke-SendMail":  ["T1114"],
    "Disable-SecuritySettings":  ["T1047"],
    "View-Email":  ["T1114"],
    "Get-SubFolders":  ["T1114"],
    "Invoke-MailSearch":  ["T1114"],
    "Get-EmailItems":  ["T1114"],
    "Invoke-SearchGAL":  ["T1114"],
    "Fetch local accounts on a member server and perform an online brute force attack":  ["T1110"],
    "HTTP-Login":  ["T1071"],
    "Get-SQLServerLoginDefaultPw":  ["T1256"],
    "Find-Fruit":  ["T1102", "T1256"],
    "Invoke-CredentialPhisher":  ["T1141", "T1514"],
    "Invoke-SauronEye":  ["T1083"],
    "Get-Screenshot":  ["T1113"],
    "Get Microsoft Updates":  ["T1082"],
    "Invoke-NinjaCopy":  ["T1105"],
    "Start-WebcamRecorder":  ["T1125"],
    "Invoke-PacketCapture":  ["T1040"],
    "Invoke-SharpLoginPrompt":  ["T1056"],
    "Out-Minidump":  ["T1033"],
    "Invoke-Inveigh":  ["T1171"],
    "Invoke-NetRipper":  ["T1179", "T1410"],
    "Invoke-WireTap":  ["T1123", "T1125", "T1056"],
    "Find-InterestingFile":  ["T1083"],
    "Get-USBKeyStrokes":  ["T1056"],
    "Get-BrowserData":  ["T1503"],
    "Get-SQLQuery":  ["T1046"],
    "Invoke-FileFinder":  ["T1083"],
    "Get-ChromeDump":  ["T1503"],
    "Get-SQLColumnSampleData":  ["T1046"],
    "Get-IndexedItem":  ["T1083"],
    "Get-KeyStrokes":  ["T1056"],
    "FoxDump":  ["T1503"],
    "Invoke-EventVwrBypass":  ["T1141", "T1514"],
    "Get-ClipboardContents":  ["T1115", "T1414"],
    "Get-SharpChromium":  ["T1503"],
    "Get-KeePassconfig":  ["T1119"],
    "Add-KeePassConfigTrigger":  ["T1119"],
    "Invoke-KeeThief":  ["T1033"],
    "Remove-KeePassConfigTrigger":  ["T1033"],
    "Find-KeePassconfig":  ["T1119"],


    }

    csvData = [['TechID', 'Software', 'Groups', 'References']]

    with open('attack.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)

        parser = argparse.ArgumentParser()
        requiredNamed = parser.add_argument_group('required named arguments')
        requiredNamed.add_argument("-a", "--Agent", action="store", dest="input_agent_file",
                                    required=False, help="Use argument (-a) to point to PowerShell Empire Agent.log file "
                                                        "or leave off argument and script will search current directory "
                                                        "and sub-directories")

        args = parser.parse_args()

        # Set flag to prevent error if no agent.log files found
        isGeneratorEmpty = True

        # Search for agent.log files based on current file path
        # https://github.com/Ar30t/attcknav_empire
        file_path = ""
        for file_path in files_within("."):
            isGeneratorEmpty = False
            if args.input_agent_file is not None and file_path is not None:
                print("Processing Empire Agent log file: " + args.input_agent_file)

                # Go through agent.log file then map ATT&CK techniques used by any PowerShell Empire modules
                with open(args.input_agent_file, 'r', newline='') as file:
                    for line in file:
                        for module, technique in techniques.items():
                            for id in technique:
                                if module in line:
                                    writer = csv.writer(csvFile)
                                    writer.writerow([id, '0', '0', '0'])
                time.sleep(10)

            else:
                print("Processing Empire Agent log file: " + file_path)

                # Go through each agent.log file then map ATT&CK techniques used by any PowerShell Empire modules
                with open(file_path, 'r', newline='') as file:
                    for line in file:
                        for module, technique in techniques.items():
                            for id in technique:
                                if module in line:
                                    writer = csv.writer(csvFile)
                                    writer.writerow([id, '0', '0', '0'])
                # csvFile.close()
                time.sleep(10)

        if args.input_agent_file is None and file_path == "":
            print("\nNo Empire agent.log file was referenced or found in current directory/sub-directories")
            exit()

if __name__ == '__main__':
    main()
    gen_layer.generate()
