import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'livisUnderscorePipe' })
export class LivisUnderscorePipe implements PipeTransform{
    transform(features: string) 
    {
        return features.replace(/_/g, ' ')
    }
}