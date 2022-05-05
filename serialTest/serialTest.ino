/** Modified code from telemetry Aim Assist Code to work without sensors. Random Data **/
#define SERIAL_RATE (115200)
#define BATV_RI 0, 100
#define ASL_RI 0, 6e3
#define AGL_RI 0, 6e3 

#define VELX_RI 0, 1e3
#define ACCX_RI 0, 1e3
#define ACCYZ_RI 0, 1e3

#define DELAY_MS 100

float f_batV;
float f_ASL;
float f_MET; 
float f_AGL; 
float f_velocityX;
float f_accelX;
float f_accelY;
float f_accelZ;
              
void setup(){
  Serial.begin( SERIAL_RATE );
  f_MET = 0;
}

void loop(){
  // Setting random vars
  f_batV =  random( BATV_RI );
  f_ASL =   random( ASL_RI );
  f_MET =   f_MET += DELAY_MS ;
  f_AGL=    random( AGL_RI );
  f_velocityX = random( VELX_RI );
  f_accelX = random( ACCX_RI );
  f_accelY = random( ACCYZ_RI );
  f_accelZ = random( ACCYZ_RI );

  sendAllTelemetry();

  delay( DELAY_MS );
}

void sendAllTelemetry() {
//  ['battery', 'lat', 'lon', 'height', 'time', 'alt', 'vx',
//                    'vy', 'vz', 'ax', 'ay', 'az', 'mx', 'my', 'mz' ]
  
  float data[] = {f_batV, 0, 0, f_ASL, f_MET, f_AGL, 
              f_velocityX, 0, 0, 
              f_accelX, f_accelY, f_accelZ,
              0,0,0};
  const int len = 15;
  
  //Serial.println("Sending telemetry");
  for(int x = 0; x < len; x++){
    Serial.print(data[x]);
    Serial.print(",");
  }
  Serial.print("\n");
    
//  data.f[0] = f_MET;
//  data.f[1] = f_pressure;
//  data.f[2] = f_ASL;
//  data.f[3] = f_AGL;
//  data.f[4] = f_velocityX;
//  data.f[5] = f_accelX;
//  data.f[6] = f_accelY;
//  data.f[7] = f_accelZ;
//  data.f[8] = f_gyrX;
//  data.f[9] = f_gyrY;
//  data.f[10] = f_gyrZ;
//  data.f[11] = f_batV;
//  data.f[12] = f_pitch;
//  data.f[13] = f_yaw;
//  data.f[14] = f_roll;
//  data.f[15] = f_oriA;
//  data.f[16] = f_oriB;
//  data.f[17] = f_oriC;
//  data.f[18] = f_oriD;
//  data.f[19] = dt;
//  data.f[20] = f_mode;
}
