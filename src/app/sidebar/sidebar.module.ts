import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SidebarNewComponent } from './sidebar-new.component';
// import { SidebarComponent } from './sidebar.component';

// @NgModule({
//     imports: [ RouterModule, CommonModule ],
//     declarations: [ SidebarComponent ],
//     exports: [ SidebarComponent ]
// })
@NgModule({
        imports: [ RouterModule, CommonModule ],
        declarations: [ SidebarNewComponent ],
        exports: [ SidebarNewComponent ]
    })
export class SidebarModule {}
