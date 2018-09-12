import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Storage } from '@ionic/storage';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

/*
  Generated class for the NodeRed provider.

  See https://angular.io/docs/ts/latest/guide/dependency-injection.html
  for more info on providers and Angular 2 DI.
*/
@Injectable()
export class NodeRedProvider {

    constructor(
        public http: Http,
        public storage: Storage) {
        
    }

    getBaseUri(): Promise<any> {

        return this.storage.get('appSettings').then((val) => {
            
            if (null != val) {
                return "http://" + val.brokerip + ":1880/";
            } else {
                return "http://127.0.0.1:1880/";
            }

        });
    }

    changeTemperature(upDown: any): Promise<any> {

        let request: any = {
            "action": upDown
        };

        //let url: string = this.nodeRedEndpoint + "temperature";
        return this.getBaseUri().then((val) => {

            let url = val + "temperature";

            return this.http.post(url, request)
                .toPromise()
                .then(this.extractData)
                .catch(this.handleError);
        });
    }

    changePowerState(onOff: any): Promise<any> {

        let request: any = {
            "action" : onOff
        };

        //let url: string = this.nodeRedEndpoint + "power";
        //return this.http.post(url, request)
        //    .toPromise()
        //    .then(this.extractData)
        //    .catch(this.handleError);

        return this.getBaseUri().then((val) => {

            let url = val + "power";

            return this.http.post(url, request)
                .toPromise()
                .then(this.extractData)
                .catch(this.handleError);
        });
    }

    getStatus(): Promise<any> {
        
        //let url: string = this.nodeRedEndpoint + "get-status";
        //return this.http.get(url)
        //    .toPromise()
        //    .then(this.extractData)
        //    .catch(this.handleError);
        //alert("yahoo");
        
        return this.getBaseUri().then((val) => {

            let url = val + "get-status";

            return this.http.get(url)
                .toPromise()
                .then(this.extractData)
                .catch(this.handleError);
        });

    }

    //'Borrowed' from //https://angular.io/docs/ts/latest/guide/server-communication.html
    private extractData(res: Response) {
        //Convert the response to JSON format
        let body = res.json();
        //Return the data (or nothing)
        return body || {};
    }

    //'Borrowed' from //https://angular.io/docs/ts/latest/guide/server-communication.html
    private handleError(res: Response | any) {
        console.error('Entering handleError');
        console.dir(res);
        return Promise.reject(res.message || res);
    }

}
