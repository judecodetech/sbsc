from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template.context import RequestContext
from django.db.models import Q
import time

from core.models import Suspect
from core.forms import FacialFeaturesForm

import logging as _logger

def index(request):

    form = FacialFeaturesForm()
    return render(request, 'sbsc/index.html', { 'form': form, } )


def ajax_suspect_search( request ):
 
    if request.is_ajax():

        facials = {
            'gender'          : request.GET.get( 'gender' ),
            'face_complexion' : request.GET.get( 'face_complexion' ),
            'face_shape'      : request.GET.get( 'face_shape' ),
            'hair'            : request.GET.get( 'hair' ),
            'cheek'           : request.GET.get( 'cheek' ),
            'ear'             : request.GET.get( 'ear' ),
            'eyelashes'       : request.GET.get( 'eyelashes' ),
            'eyebrow'         : request.GET.get( 'eyebrow' ),
            'eyes'            : request.GET.get( 'eyes' ),
            'nose'            : request.GET.get( 'nose' ),
        }

        for key, value in facials.iteritems():
            if value == '<select' or value is None:
                facials[key] = ''

        for key, value in facials.iteritems():
            if value != '':
                #if choice.strip():            
                results = Suspect.objects.filter( 
                    Q( gender__icontains = facials['gender'] ) &
                    Q( face_complexion__icontains = facials['face_complexion'] ) &
                    Q( face_shape__icontains = facials['face_shape'] ) &
                    Q( hair__icontains = facials['hair'] ) &
                    Q( cheek__icontains = facials['cheek'] ) &
                    Q( ear__icontains = facials['ear'] ) &
                    Q( eyelashes__icontains = facials['eyelashes'] ) &
                    Q( eyebrow__icontains = facials['eyebrow']) &
                    Q( eyes__icontains = facials['eyes'] ) &
                    Q( nose__icontains = facials['nose'] ) 
                )

        return render( request, 'sbsc/results.html', { 'results': results, } )
