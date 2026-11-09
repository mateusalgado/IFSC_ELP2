#!/bin/bash
# roda todos os casos em sequencia e gera as figuras; log em runs/batch.log
cd /mnt/c/Users/mateu/OneDrive/Documentos/ELP2/PROJETO/03_Simulacao
CASOS=$(python3 -c "import gera_netlist as g; print(' '.join(g.CASOS))")
for c in $CASOS; do
  python3 roda.py $c
  python3 plota.py $c
done
echo "BATCH DONE $(date)"
