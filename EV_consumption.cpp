#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#define slice 10
#define max_route_size 100000000

float Gravity=9.8;			//gravity factor 9.8 m/s^2

float rd[max_route_size],rs[max_route_size],rv[max_route_size];
int r_count=0;

struct vehicle{
	float MotorEfficiency; 		//vehicle motor output efficiency
	float ChargeEfficiency;		//vehicle charge efficiency while breaking
	float Weight; 				//vehicle weight in KG
	float RollingResistance; 	//vehicle tyre rolling resistance
	float AirResistance; 		//vehicle air resistance
	float FrontalArea;			//vehicle frontal area
	int type;					//vehicle type 0:electric 1:gasoline 2:diesel
}tesla,corolla;

//distance in meter,slope in rad,v1v2 in m/s
float calc_consumption(float distance,float slope,float v1,float v2,vehicle car){
	
	float m=car.Weight; 			//mass
	float g=Gravity;				//gravity factor
	float f=car.RollingResistance; 	//rolling resistance
	float Cd=car.AirResistance; 	//air resistance
	float A=car.FrontalArea;		//frontal area
	float d=distance;
	float deg=slope;
	
	//Time required
	float t=2*d/(v1+v2);
	
	//Potential Energy
	float potential=m*g*d*sin(deg);
	//printf("potential=%f Joules\n",potential);
	
	//Kinetic Energy
	float kinetic=m*(v2*v2-v1*v1)/2.0;
	//printf("kinetic=%f Joules\n",kinetic);
	
	//Tyre rolling Energy
	float rolling=m*g*f*d;
	//printf("rolling=%f Joules\n",rolling);
	
	//Air Energy
	float air=0.0;
	float dv=(v2-v1)/((float)slice);
	float dt=t/(float)slice;
	float v;
	for(int i=0,v=v1;i<slice;v+=dv,++i){
		air+=(Cd*A*v*v/21.15)*dv*dt;
	}
	//printf("air=%f Joules\n",air);
	
	//Overall
	float overall=potential+kinetic+rolling+air;
	//printf("overall=%f Joules\n",overall);
	
	//energy
	float energy;
	if(overall>0.0) energy=overall/car.MotorEfficiency;
	else if(car.ChargeEfficiency>0.0) energy=overall*car.ChargeEfficiency;
	else energy=0.0;
	
	//Power
	float power=energy/t;
	//printf("power=%f Watt (t=%f)\n",power,t);
	
	return energy;
}

float calc_constant_speed(float distance,float slope,float v,vehicle car){
	
	float m=car.Weight; 			//mass
	float g=Gravity;				//gravity factor
	float f=car.RollingResistance; 	//rolling resistance
	float Cd=car.AirResistance; 	//air resistance
	float A=car.FrontalArea;		//frontal area
	float d=distance;
	float deg=slope;
	
	//Time required
	float t=d/v;
	
	//Potential Energy
	float potential=m*g*d*sin(deg);
	//printf("potential=%f Joules\n",potential);
	
	//Tyre rolling Energy
	float rolling=m*g*f*d;
	//printf("rolling=%f Joules\n",rolling);
	
	//Air Energy
	float air=d*Cd*A*v*v/21.15;
	//printf("air=%f Joules\n",air);
	
	//Overall I/O energy
	float overall=potential+rolling+air;
	//printf("overall=%f Joules\n",overall);
	
	//Battery energy
	float energy;
	if(overall>0.0) energy=overall/car.MotorEfficiency;
	else if(car.ChargeEfficiency>0.0) energy=overall*car.ChargeEfficiency;
	else energy=0.0;
	
	//Power
	float power=energy/t;
	//printf("power=%f Watt (t=%f)\n",power,t);
	
	return energy;
}

float calc_kinetic_energy(float v1,float v2,vehicle car){
	
	float m=car.Weight; 			//mass
	
	//Kinetic Energy
	float kinetic=m*(v2*v2-v1*v1)/2.0;
	//printf("kinetic=%f Joules\n",kinetic);

	//Overall I/O energy
	float overall=kinetic;
	//printf("overall=%f Joules\n",overall);
	
	//Battery energy
	float energy;
	if(overall>0.0) energy=overall/car.MotorEfficiency;
	else if(car.ChargeEfficiency>0.0) energy=overall*car.ChargeEfficiency;
	else energy=0.0;

	return energy;
}



int main(int argc, char** argv)
{
	tesla.MotorEfficiency=0.81*0.5; //0.81 battery output converter , 0.5 motor output to tyres
	tesla.ChargeEfficiency=0.3;		
	tesla.Weight=2108;				//actual value 
	tesla.RollingResistance=0.012;
	tesla.AirResistance=0.24;		//actual value https://en.wikipedia.org/wiki/Automobile_drag_coefficient
	tesla.FrontalArea=2.3258018;	//actual value https://my.teslamotors.com/it_CH/forum/forums/need-moreverifying-information-model-s
	tesla.type=0;					//electric
	
	corolla.MotorEfficiency=0.29;
	corolla.ChargeEfficiency=0.0;
	corolla.Weight=1235;
	corolla.RollingResistance=0.012;
	corolla.AirResistance=0.29;
	corolla.FrontalArea=2.0903184;
	corolla.type=1;
	
	vehicle mycar;
//	mycar=tesla;
	mycar=corolla;
	if (argc > 2 && argv[2][0]=='t') {
		mycar=tesla;
	}
	else {
		mycar=corolla;
	}
	
//	char inputfile[]="dsv_HtY_mi1.txt";
	char *inputfile = argv[1];
	
	FILE *fp;
	if( (fp=fopen(inputfile,"r")) == NULL ){
		puts("open file error!!");
		exit(1);
	}
	
	float total_d=0.0;
	
//	while(!feof(fp)){
//		fscanf(fp,"%f %f %f",&rd[r_count],&rs[r_count],&rv[r_count]);
	while(fscanf(fp,"%f %f %f",&rd[r_count],&rs[r_count],&rv[r_count]) == 3) {
		printf("%f %f %f\n",rd[r_count],rs[r_count],rv[r_count]);
		if(rd[r_count]!=0.0) r_count++;
	}

//	getchar();
	printf("a");
	
	float d_eng,d_kin,total_eng=0;
	int i;
	for(i=0;i<r_count-1;++i){
		d_eng=calc_constant_speed(rd[i],rs[i],rv[i],mycar);
		d_kin=calc_kinetic_energy(rv[i],rv[i+1],mycar);
		total_eng+=d_eng+d_kin;
		total_d+=rd[i];
		printf("d=%f s=%f v=%f de=%f dk=%f total=%f\n",rd[i],rs[i],rv[i],d_eng,d_kin,total_eng);
	}
	total_d+=rd[i];
	d_eng=calc_constant_speed(rd[i],rs[i],rv[i],mycar);
	total_eng+=d_eng;
	printf("d=%f s=%f v=%f de=%f total=%f\n",rd[i],rs[i],rv[i],d_eng,total_eng);
	
	printf("total: energy=%f Jouels   distance=%f km\n",total_eng,total_d/1000.0);
	if(mycar.type==0){ //electric
		//1kwh=1000*3600=3 600 000 Jouels
		float total_kwh=total_eng/3600000.0;
		float total_km=total_d/1000.0;
		printf("battery=%f kwh consumption=%f km/kwh\n",total_kwh,total_km/total_kwh);		
	}
	else if(mycar.type==1){ //fuel
		//1L=5 600 000 Jouels
		float total_L=total_eng/5600000.0;
		float total_km=total_d/1000.0;
		printf("fuel=%f L consumption=%f km/L\n",total_L,total_km/total_L);
	}

/*	
	puts("\nOriginalFunction:");
	printf("BatteryChanged=%f Joules\n",calc_consumption(25.0,0.174532925,5,10,tesla));
	//from 5m/s to 10m/s within 25meter on slope 10degree
	
	float energy;
	puts("\nConstant Speed:");
	energy=calc_constant_speed(25.0,0.174532925,10,tesla); 	//energy required for run 25meter in 0.17453rad (10 degree) slope 
															//with constant speed 10m/s
	puts("\nKinetic Energy");
	energy=calc_kinetic_energy(5,10,tesla); //energy required for acceleration from 5m/s to 10m/s
*/	
	
}





