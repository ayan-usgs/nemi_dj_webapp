

from django.forms import ModelChoiceField, ChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple, TextInput, Textarea
from django.forms import CharField, IntegerField, URLField

from common.models import StatisticalDesignObjective, StatisticalItemType, COMPLEXITY_CHOICES, LEVEL_OF_TRAINING_CHOICES, StatisticalAnalysisType, StatisticalSourceType
from common.models import MediaNameDOM, StatisticalTopics, MethodSourceRef, StatAnalysisRelStg, StatDesignRelStg, StatTopicRelStg, StatMediaRelStg
from common.models import PublicationSourceRelStg

from domhelp.forms import BaseDefinitionsForm

 
class StatMethodEditForm(BaseDefinitionsForm):
    
    sam_source_method_identifier = CharField(max_length=30,
                                         widget=TextInput(attrs={'size' : 30}))
    sam_method_official_name = CharField(max_length=250,
                                     widget=Textarea(attrs={'rows' : 3, 'cols' : 50}))
    sam_method_source = ModelChoiceField(queryset=MethodSourceRef.objects.all(),
                                     required=False)
    country = CharField(max_length=100, 
                        required=False)
    author = CharField(max_length=450, 
                       widget=Textarea(attrs={'rows': 3, 'cols' : 50}))
    sam_brief_method_summary = CharField(max_length=4000, 
                                     widget=Textarea(attrs={'rows' : 10, 'cols' : 50}))
    table_of_contents = CharField(max_length=1000, 
                                  required=False, 
                                  widget=Textarea(attrs={'rows': 10, 'cols' : 50}))
    publication_year = IntegerField(max_value=9999, 
                                    min_value=0,
                                    widget=TextInput(attrs={'size': 4}))
    source_citation_name = CharField(max_length=450, 
                                     widget=Textarea(attrs={'rows' : 9, 'cols' : 50}))
    link_to_full_method = URLField(max_length=240, 
                                   required=False,
                                   widget=TextInput(attrs={'size' : 50}))
    notes = CharField(max_length=2000, 
                         required=False, 
                         widget=Textarea(attrs={'rows' : 9, 'cols' : 50}))
    item_type = ModelChoiceField(queryset=StatisticalItemType.objects.all())
    item_type_note = CharField(max_length=50, 
                               required=False,
                               widget=TextInput(attrs={'size' : 50}))
    sponser_types = ModelMultipleChoiceField(queryset=StatisticalSourceType.objects.all(), 
                                             widget=CheckboxSelectMultiple)
    sponser_type_note = CharField(max_length=50, 
                                  required=False,
                                  widget=TextInput(attrs={'size': 50}))
    analysis_types = ModelMultipleChoiceField(queryset=StatisticalAnalysisType.objects.all(), 
                                              widget=CheckboxSelectMultiple)
    design_objectives = ModelMultipleChoiceField(queryset=StatisticalDesignObjective.objects.all(), 
                                                 widget=CheckboxSelectMultiple)
    sam_complexity = ChoiceField(choices=[('', '-------')] + COMPLEXITY_CHOICES)
    level_of_training = ChoiceField(choices=[('' ,'--------')] + LEVEL_OF_TRAINING_CHOICES)
    media_emphasized = ModelMultipleChoiceField(queryset=MediaNameDOM.stat_media.all(),
                                                widget=CheckboxSelectMultiple)
    media_emphasized_note = CharField(max_length=50, 
                                      required=False,
                                      widget=TextInput(attrs={'size' : 50}))
    media_subcategory = CharField(max_length=150, 
                                  required=False,
                                  widget=TextInput(attrs={'size' : 50}))
    special_topics = ModelMultipleChoiceField(queryset=StatisticalTopics.objects.all(), 
                                              required=False,
                                              widget=CheckboxSelectMultiple)
        
    def get_source_citation_object(self, obj):
        ''' Returns obj with the SourceCitationRef fields filled in from the form's cleaned data
        This method assumes that the form has been validated and that cleaned_data attribute is available and
        obj should be a SourceCitationRef object.
        '''
        data = self.cleaned_data
        obj.source_citation = data['sam_source_method_identifier']
        obj.title = data['sam_method_official_name']
        obj.country = data['country']
        obj.author = data['author']
        obj.table_of_contents = data['table_of_contents']
        obj.publication_year = data['publication_year']
        obj.source_citation_name = data['source_citation_name']
        obj.link = data['link_to_full_method']
        obj.item_type = data['item_type']
        obj.item_type_note = data['item_type_note']
        obj.sponser_type_note = data['sponser_type_note']
        
        return obj
    
    def get_publication_sources(self, source_citation_ref_id):
        ''' Returns the list of PublicationSourceRelStg objects associated with source_citation_ref_id'''
        result = [PublicationSourceRelStg(source_citation_ref_id=source_citation_ref_id, source=t) for t in self.cleaned_data['sponser_types']]
        return result
        
    def get_method_object(self, obj):
        ''' Returns obj with the MethodAbstract fields filled in from the form's cleaned data.
        This method assumes that the form has been validated and that the cleaned data attribute is available and
        that object is a descendant of MethodAbstract.
        '''
        data = self.cleaned_data
        
        obj.method_source = data['sam_method_source']
        obj.source_method_identifier = data['sam_source_method_identifier']
        obj.method_descriptive_name = data['source_citation_name']
        obj.method_official_name = data['sam_method_official_name']
        obj.brief_method_summary = data['sam_brief_method_summary']
        obj.link_to_full_method = data['link_to_full_method']
        obj.notes = data['notes']
        obj.sam_complexity = data['sam_complexity']
        obj.level_of_training = data['level_of_training']
        obj.media_emphasized_note = data['media_emphasized_note']
        obj.media_subcategory = data['media_subcategory']
        
        return obj
 
    def get_analysis_types(self, method_id):
        '''Returns a list of StatAnalysisRelStg objects associated with method_id'''
        result = [StatAnalysisRelStg(method_id=method_id, analysis_type=t) for t in self.cleaned_data['analysis_types']]
        return result
        
    def get_design_objectives(self, method_id):
        '''Returns a list of StatDesignRelStg objects associated with method_id'''
        result = [StatDesignRelStg(method_id=method_id, design_objective=t) for t in self.cleaned_data['design_objectives']]
        return result
    
    def get_media_emphasized(self, method_id):
        '''Returns a list of StatMediaRelStg objects associated with method_id'''
        result = [StatMediaRelStg(method_id=method_id, media_name=t) for t in self.cleaned_data['media_emphasized']]
        return result
    
    def get_special_topics(self, method_id):
        '''Returns a list of StatTopicRelStg objects associated with method_id'''
        result = [StatTopicRelStg(method_id=method_id, topic=t) for t in self.cleaned_data['special_topics']]
        return result
    