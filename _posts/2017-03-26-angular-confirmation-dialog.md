---
layout: blog-post
title: "Angular2 Confirmation Dialog component"
excerpt: "Angular2 Confirmation Dialog component"
disqus_id: /2017/03/26/angular-confirmation-dialog-component/
tags:
- Angular
- Typescript
---


Recently, I have been working on Angular2 quite a lot. We had a requirement to come up with a reusable confirmation dialog component. Below is the quick implementation I came up with. I will
soon wrap it into a npm module. Any feedbacks?


`confirmation-dialog.component.ts`
{% highlight typescript %}
import { Component, OnInit } from '@angular/core';
import { MdDialogRef } from '@angular/material';

@Component({
	selector: 'app-confirmation-dialog',
	templateUrl: './confirmation-dialog.component.html',
	styleUrls: ['./confirmation-dialog.component.scss']
})
export class ConfirmationDialogComponent implements OnInit {
	public title: string;
	public message: string;
	public titleAlign?: string;
	public messageAlign?: string;
	public btnOkText?: string;
	public btnCancelText?: string;
	constructor(public dialogRef: MdDialogRef<ConfirmationDialogComponent>) { }

	ngOnInit() {
	}

}
{% endhighlight %}

`confirmation-dialog.service.ts`
{% highlight typescript %}
import { Observable } from 'rxjs/Rx';
import { ConfirmationDialogComponent } from './confirmation-dialog.component';
import { MdDialogRef, MdDialog, MdDialogConfig } from '@angular/material';
import { Injectable, ViewContainerRef } from '@angular/core';

@Injectable()
export class ConfirmationDialogsService {

    constructor(private dialog: MdDialog) { }

    public confirm(title: string, message: string, viewContainerRef: ViewContainerRef, btnOkText: string ='Ok', btnCancelText: string ='Cancel'): Observable<boolean> {

        let dialogRef: MdDialogRef<ConfirmationDialogComponent>;
        let config = new MdDialogConfig();
        config.viewContainerRef = viewContainerRef;

        dialogRef = this.dialog.open(ConfirmationDialogComponent, config);

        dialogRef.componentInstance.title = title;
        dialogRef.componentInstance.message = message;
        dialogRef.componentInstance.btnOkText = btnOkText;
        dialogRef.componentInstance.btnCancelText = btnCancelText;

        return dialogRef.afterClosed();
    }

     public confirmWithoutContainer(title: string, message: string, titleAlign: string='center', messageAlign: string='center', btnOkText: string ='Ok', btnCancelText: string ='Cancel' ): Observable<boolean> {

        let dialogRef: MdDialogRef<ConfirmationDialogComponent>;
        let config = new MdDialogConfig();
        // config.viewContainerRef = viewContainerRef;

        dialogRef = this.dialog.open(ConfirmationDialogComponent, config);

        dialogRef.componentInstance.title = title;
        dialogRef.componentInstance.message = message;
        dialogRef.componentInstance.titleAlign = titleAlign;
        dialogRef.componentInstance.messageAlign = messageAlign;
        dialogRef.componentInstance.btnOkText = btnOkText;
        dialogRef.componentInstance.btnCancelText = btnCancelText;

        return dialogRef.afterClosed();
    }
}
{% endhighlight %}


`confirmation-dialog.component.html`
{% highlight html %}
<div class="box-holder">
   <div class="header-row"  [ngClass]="{'text-center-align': titleAlign=='center', 'text-right-align': titleAlign=='right' }"fxLayoutAlign="space-between center">
       <div class="header-title ">
           {{ title }}
       </div>
   </div>
   <div class="content-holder" [ngClass]="{'text-center-align': messageAlign=='center', 'text-right-align': messageAlign=='right' }" fxLayoutAlign="start start">
       {{ message }}
   </div>
   <div class="action-container" fxLayoutAlign="end end">
       <button type="button" md-button class="od-button od-ripple action-button" (click)="dialogRef.close()">{{ btnCancelText }}</button>
        <button type="button" md-raised-button class="od-button od-ripple action-button" (click)="dialogRef.close(true)"> {{ btnOkText }} </button>
   </div>
</div>
{% endhighlight %}