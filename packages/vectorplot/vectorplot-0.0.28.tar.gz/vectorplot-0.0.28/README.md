# vectorplot

**vectorplot** é um pacote simples e fácil para plotar vetores no espaço bidimensional e tridimensional.

## Dependências
**Python 3.6** ou posterior

Pacote **numpy**
Pacote **matplotlib.pyplot**


## Começando o uso
Você vai precisar instalar o pacote **vectorplot**, para isso basta executar:
```
pip install vectorplot
```

## Funções

* `plot2d([<lista de componentes de vetores>],[<lista de cores para cada vetor],[<limites da plotage 2D>])` - Plota vetores a partir de componentes no espaço bidimensional
```
Ex: 
pip install vectorplot
import numpy as np
from vectorplot import vp

u_laranja='#FF9A13'
v_azul='#1190FF'
r_vermelho='#FF0000'

u=[1,2]
v=[2,1]
u=np.array(u)
v=np.array(v)
r=u+v

vp.plot2d([u,v,r], [u_laranja,v_azul,r_vermelho], [-3,3,-3,3])
```

* `plot2d([<Lista de tuplas de coordenadas>],[<lista de cores para cada vetor],[<limites da plotage 2D>])` - Plota vetores a partir de tuplas de coordenadas de pontos no espaço bidimensional
```
Ex: 
pip install vectorplot
from vectorplot import vp

#As tuplas devem conter coordenadas iniciais (xi,yi) e finais (xf,yf) por onde passa o vetor 
u=(1,1,4,4)
v=(-1,2,5,6)
u_laranja='#FF9A13'
v_azul='#1190FF'
vp.plot2d([u,v], [u_laranja,v_azul], [-6,6,-6,6])
```


* `plot3d([<lista de componentes de vetores>],[<lista de cores para cada vetor],[<limites da plotage 3D>])` - Plota vetores a partir de componentes no espaço tridimensional
```
Ex: 
pip install vectorplot
import numpy as np
from vectorplot import vp

u_laranja='#FF9A13'
v_azul='#1190FF'
r_vermelho='#FF0000'

u=[-1,1,2]
v=[2,3,2]
u=np.array(u)
v=np.array(v)
r=u+v

vp.plot3d([u,v,r],[u_laranja,v_azul,r_vermelho],[-4,4,-4,4,-4,4])
```

* `plot3d([<Lista de tuplas de coordenadas>],[<lista de cores para cada vetor],[<limites da plotage 3D>])` - Plota vetores a partir de tuplas de coordenadas de pontos no espaço tridimensional
```
Ex: 
pip install vectorplot
import numpy as np
from vectorplot import vp

u_laranja='#FF9A13'
v_azul='#1190FF'

u=(-1,1,2,2)
v=(2,3,4,5]

vp.plot3d([u,v],[u_laranja,v_azul],[-5,5,-5,5,-5,5])
```

* `equivalent2d([<Lista de componentes de vetores>])` - Verifica se uma lista de vetores 2d gerada a partir de componentes são equivalentes
```
Ex: 
pip install vectorplot
from vectorplot import vp

u=[2,2]
v=[2,2]
print(vp.isequivalent([u,v]))

```

* `equivalent2d([<Lista de tuplas de coordenadas>])` - Verifica se uma lista de vetores 2d gerada a partir de tuplas de coordenadas de pontos são equivalentes
```
Ex: 
pip install vectorplot
from vectorplot import vp

u=(1,1,4,4)
v=(-1,2,5,6)
print(vp.isequivalent([u,v]))

```
* `equivalent3d([<Lista de componentes de vetores>])` - Verifica se uma lista de vetores 3d gerada a partir de componentes são equivalentes
```
Ex: 
pip install vectorplot
from vectorplot import vp

u=[2,2,2]
v=[2,2,2]
print(vp.isequivalent([u,v]))

```

* `equivalent3d([<Lista de tuplas de coordenadas>])` - Verifica se uma lista de vetores 3d gerada a partir de tuplas de coordenadas de pontos são equivalentes
```
Ex: 
pip install vectorplot
from vectorplot import vp

u=(1,1,1,4,4)
v=(0,0,0,3,3,3)
print(vp.isequivalent([u,v]))

```

* `resultant_module(<módulo do primeiro vetor>,<módulo do segundo vetor>,<ângulo formando entre vetores)` - Calcula o módulo da resultante gerado a partir de um ângulo entre dois vetores
```
Ex: 
pip install vectorplot
from vectorplot import vp

print(vp.resultant_module_angle(2,2,60))

```


* `vector_module(<vetor>)` - Calcula o módulo do vetor a partir dos seus componentes
```
Ex: 
pip install vectorplot
from vectorplot import vp
v=[2,2,1]
print(vp.vector_module(v))
v=[1,1]
print(vp.vector_module(v))
```


* `angle_vectors(vector 1, vector 2)` - Calcula o angulo entre dois vetores
```
Ex: 
pip install vectorplot
from vectorplot import vp
v=[1,0]
u=[0,1]
print(vp.angle_vectors(v,u))
```