"""
calcul de pi avec la méthode d'archimede
seule pi_val3 donne les bonnes décimales de pi avec nb_iteration=1000
"""

nb_iteration = 20

cn = 1
for n in range(nb_iteration):
    # nombre de côté pour n+1
    nb_c = 3 * 2**(n+1)
    # longueur du côté n+1
    cn_1 = ((cn/2)**2 + (1 - (1-(cn/2)**2)**0.5)**2)**0.5
    pi_val = nb_c * cn_1
    cn = cn_1

cn = 1
for n in range(nb_iteration):
    nb_c = 3 * 2**(n+1)
    cn_1 = (2 *(1 - (1-(cn/2)**2)**0.5))**0.5
    pi_val2 = nb_c * cn_1
    cn = cn_1

cn = 1
for n in range(nb_iteration):
    nb_c = 3 * 2**(n+1)
    deno_2 = 2 + 2 * (1 - (cn/2)**2)**0.5
    cn_1 = cn / deno_2**0.5
    pi_val3 = nb_c * cn_1
    cn = cn_1

print(pi_val)
print(pi_val2)
print(pi_val3)
