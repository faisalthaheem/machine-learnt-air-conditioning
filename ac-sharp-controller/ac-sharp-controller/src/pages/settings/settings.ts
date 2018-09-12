import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { Storage } from '@ionic/storage';
import { AlertController } from 'ionic-angular';

/*
  Generated class for the settings page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
    selector: 'page-settings',
    templateUrl: 'settings.html'
})
export class SettingsPage {

    settingsContext = {};

    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        private storage: Storage,
        public alertCtrl: AlertController
    ) { }

    ionViewWillEnter() {

        this.storage.get('appSettings').then((val) => {
            if (null == val) {
                val = {};
                val.brokerip = "undefined";
            }
            this.settingsContext = val;
        });
    }

    saveSettings() {

        let alert = this.alertCtrl.create({
            title: 'Settings Saved!',
            subTitle: 'Settings have successfully been saved.',
            buttons: ['OK']
        });

        this.storage.set('appSettings', this.settingsContext).then(function () {
            alert.present();
        });
    }
}
