<?php
//crontab: ps -ef| grep -v grep | grep pmAutoCheck.php ;if [ $? -ne 0 ];then /usr/bin/php pmAutoCheck.php 2>&1 >/dev/null &;fi
set_time_limit(0); 
//获取pm2信息
$comGetPm2Info="pm2 jlist";
$pm2OutPut = "";
$pm2OutPut=exec($comGetPm2Info);

//解析json

$pm2Info = json_decode($pm2OutPut,true);
$pm2InstanceNum = count($pm2Info);

//重启PM2进程
function restartPm2Instance($pm_id){
        $commRestart = "pm2 restart ".$pm_id;
        system($commRestart);
}

//通过检查日志是否有变化
//来确定PM2进程是否在处理请求
function isLogModified($pm2Info,$pm_id){
    $pm2InstanceLog = $pm2Info[$pm_id]['pm2_env']['pm_out_log_path'];
    if( file_exists($pm2InstanceLog)){
        $lastModified = filemtime($pm2InstanceLog);
        sleep(5);
        $newModified = filemtime($pm2InstanceLog);
        if( $newModified <= $lastModified ){
            echo "file not modifed";
            return 0;
        }else{
            return 1;
        }
        
    }else {
        return 2;
    }
}

//死循环，间隔60s来检查一次
while(1){
for( $i=0 ;$i<$pm2InstanceNum ;$i++){
    $pm2InstanceLoad = (int)round( $pm2Info[$i]['monit']['cpu']);
    $pm_id = $pm2Info[$i]['pm_id'];
    if( $pm2InstanceLoad >= 90 ){
        $needRestart = isLogModified($pm2Info,$pm_id);
        if( $needRestart == 0 ){
            restartPm2Instance($pm_id);
        }
    }

}
    sleep(60);
}
