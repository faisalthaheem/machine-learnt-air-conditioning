import { Component } from '@angular/core';
import { NavController, Platform } from 'ionic-angular';
import { NodeRedProvider } from "../../providers/NodeRed";
import { Storage } from '@ionic/storage';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

    systemState: any = {
        "powerMode": "?",
        "temperature" : "?"
    };

    constructor(
        public navCtrl: NavController,
        public platform: Platform,
        public nrProv: NodeRedProvider, 
        public storage: Storage
    ) {

    }

    ionViewDidEnter(){

        this.platform.ready().then((readySource) => {
            this.storage.ready().then(() => {

                this.getStatus();
            });
        });
        
    }

    getStatus() {

        this.nrProv.getStatus().then(
            data => {
                if (data && data.currentACState) {

                    if (data.currentACState == 1) {
                        this.systemState.powerMode = "on";
                    } else {
                        this.systemState.powerMode = "off";
                    }

                    this.systemState.temperature = data.currTemperature;
                }
            },
            error => {
                console.error('Error retrieving data');
                this.systemState.powerMode = "Err";
                this.systemState.temperature = "Err";
                console.dir(error);

            }
        );
    }   

  onPowerOn() {
      
      this.nrProv.changePowerState(1).then(
          data => {

              if (data && data.action && data.action == 1) {
                  this.systemState.powerMode = "on";
              } else {
                  this.systemState.powerMode = "off";
              }
          },
          error => {
              console.error('Error retrieving data');
              this.systemState.powerMode = "Err";
              console.dir(error);
              
          }
      );
  }

  onPowerOff() {
      
      this.nrProv.changePowerState(0).then(
          data => {

              if (data && data.action && data.action == 1) {
                  this.systemState.powerMode = "on";
              } else {
                  this.systemState.powerMode = "off";
              }
          },
          error => {
              console.error('Error retrieving data');
              this.systemState.powerMode = "Err";
              console.dir(error);

          }
      );
  }


  onTempDown() {

      this.nrProv.changeTemperature("down").then(
          data => {
              
              this.systemState.temperature = "" + data;
          },
          error => {
              console.error('Error retrieving data');
              this.systemState.powerMode = "Err";
              console.dir(error);

          }
      );
  }

  onTempUp() {

      this.nrProv.changeTemperature("up").then(
          data => {
              
              this.systemState.temperature = "" + data;
          },
          error => {
              console.error('Error retrieving data');
              this.systemState.powerMode = "Err";
              console.dir(error);

          }
      );
  }

}
