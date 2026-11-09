# Reimplementacao das formulas da aba "Toroid Design" (Magnetics Inductor Design Tool), material MPP 125u
$L=0.096; $Idc=8.33; $dI=0.833; $f=100; $Ta=25
$Irms_rip = $dI/2/1.732; $Imax=$Idc+$dI/2; $Imin=$Idc-$dI/2
# MPP 125u
$a=0.01; $b=1.96711260614526E-006; $c=2.25345696165796
$na=0.000642; $nb=-0.0006271; $nc=0.0003253; $nd=0.009901; $ne=0.0005366; $nx=0.5
$cla=53.05; $clb=2.06; $clc=1.56
$cores = @{
 '55930'=@{AL=157;le=6.35;Wa=1.56;Ve=4.15;OD=27.69;ID=14.1;HT=12;Ae=0.654;slope=227500;icpt=2470}
 '55548'=@{AL=127;le=8.14;Wa=2.97;Ve=5.34;OD=33.66;ID=19.4;HT=11.5;Ae=0.656;slope=412500;icpt=3150}
 '55254'=@{AL=168;le=9.84;Wa=4.27;Ve=10.6;OD=40.77;ID=23.3;HT=15.4;Ae=1.07;slope=580000;icpt=4840}
}
$wires = @{ 13=@(5184,0.0284); 14=@(4109,0.0231); 15=@(3260,0.0184); 16=@(2581,0.01472); 17=@(2052,0.01177); 18=@(1624,0.00942); 19=@(1289,0.00754); 20=@(1024,0.00607); 21=@(812.3,0.00484); 22=@(640.1,0.00386)}
function pm($H){ 0.01/($a+$b*[math]::Pow($H,$c)) }
function Design($pn,$awg,$ns,$Nfix){
 $k=$cores[$pn]; $ALmin=$k.AL*0.92
 $N0=[math]::Ceiling([math]::Sqrt($L*1e6/$ALmin))
 $N= if($Nfix){$Nfix}else{[math]::Ceiling($N0/(pm ($Idc*$N0/$k.le)))}
 $Lmax=$ALmin*(pm ($Imax*$N/$k.le))*$N*$N/1e6
 $Lavg=$ALmin*(pm ($Idc*$N/$k.le))*$N*$N/1e6
 $L0=$k.AL*$N*$N/1e6
 $cm=$wires[$awg][0]; $area=$wires[$awg][1]*$ns
 $FF=$area*$N/$k.Wa
 $wod=[math]::Sqrt(4*$area*100/[math]::PI)
 $circ1=2*[math]::PI*($k.ID/2-$wod/2); $tpl=[math]::Floor($circ1/$wod)
 $t1=[math]::Min($tpl,$N); $r=$N-$t1; $t2= if($r -le 0){0}elseif($r -ge $t1-6){$t1-6}else{$r}
 $r=$N-$t1-$t2; $t3= if($r -le 0){0}elseif($r -ge $t2-6){$t2-6}else{$r}
 $r=$N-$t1-$t2-$t3; $t4= if($r -le 0){0}elseif($r -ge $t3-6){$t3-6}else{$r}
 $wc=$k.OD-$k.ID+2*$k.HT; $s3=[math]::Sqrt(3)
 $len=$t1*($wc+4*$wod)+$t2*($wc+8*($wod/2+$s3*$wod/2))+$t3*($wc+8*$wod/2+16*$s3*$wod/2)+$t4*($wc+8*$wod/2+24*$s3*$wod/2)
 $MLT=$len/$N; $Rpm=10.371/$cm*3.281/$ns
 $DCR=$MLT*$N*$Rpm/1000*1000   # mOhm
 $Pcu=$Idc*$Idc*$DCR/1000+$Irms_rip*$Irms_rip*$DCR*2.5/1000
 $Hmax=$N/$k.le*$Imax; $Hmin=$N/$k.le*$Imin
 $BH={param($H) [math]::Pow(($na+$nb*$H+$nc*$H*$H)/(1+$nd*$H+$ne*$H*$H),$nx)}
 $Bpk=((& $BH $Hmax)-(& $BH $Hmin))/2
 $Pfe=$cla*[math]::Pow($Bpk,$clb)*[math]::Pow($f,$clc)*$k.Ve/1000
 $SA=0.01*($k.slope*(0.01*$FF)+$k.icpt)
 $dT=[math]::Pow(($Pfe+$Pcu)*1000/$SA,0.833)
 $layers=@($t1,$t2,$t3,$t4 | Where-Object {$_ -gt 0}).Count
 $fits = ($t1+$t2+$t3+$t4) -ge $N
 [pscustomobject]@{PN=$pn;AWG=$awg;Fios=$ns;N=$N;L0_uH=[math]::Round($L0*1000,1);Lavg_uH=[math]::Round($Lavg*1000,1);Lmax_uH=[math]::Round($Lmax*1000,1);'%u_Imax'=[math]::Round(100*(pm $Hmax),1);H_Acm=[math]::Round($Hmax,1);FF=[math]::Round($FF,3);Camadas=$layers;Cabe=$fits;MLT=[math]::Round($MLT,1);Fio_m=[math]::Round($len/1000,2);DCR_mOhm=[math]::Round($DCR,2);Bpk_mT=[math]::Round($Bpk*1000,2);Pnuc_mW=[math]::Round($Pfe*1000,1);Pcu_W=[math]::Round($Pcu,3);Ptot_W=[math]::Round($Pfe+$Pcu,3);SA_cm2=[math]::Round($SA,1);dT=[math]::Round($dT,1)}
}
$res = @(); $res += Design '55930' 13 1 42
$res += Design '55930' 13 1 $null
foreach($w in @(@(14,1),@(15,1),@(16,2),@(17,2),@(18,3),@(19,4),@(20,5),@(21,6),@(22,8))){ $res += Design '55930' $w[0] $w[1] $null }
foreach($w in @(@(13,1),@(15,2),@(16,2),@(17,3),@(18,4))){ $res += Design '55548' $w[0] $w[1] $null }
foreach($w in @(@(13,1),@(16,2))){ $res += Design '55254' $w[0] $w[1] $null }
$res | ConvertTo-Csv -NoTypeInformation -Delimiter ";"
