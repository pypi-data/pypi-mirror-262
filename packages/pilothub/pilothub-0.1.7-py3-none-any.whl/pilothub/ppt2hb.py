from pilothub.pptx2content import PPTxFile

class PPTxToHB(PPTxFile):
    def __init__(self, file_path):
        super().__init__(file_path)

    def get_handbook_from_ppt(self, output_path: str, 
                              content_client,
                              SET_SLIDE_TEXT_FOR_SKIP_SLIDES: bool = True,
                              SET_AI_TEXT_FOR_SKIP_SLIDES: bool = False,
                              AI_PROPMT_SKIP_SLIDES: str = None,
                              AI_PROMPT_DICT_SKIP_SLIDES: dict[str, str] = None,
                              DEFAULT_PROMPT_FOR_OTHER_SLIDES: str = None,
                              SKIP_NOTES_FOR_SLIDES_WITH_NOTES: bool = False,
                              ):
        """
        Write notes to the PPTx file.
        :param output_path: Path to save the PPTx file.
        :param content_client: Content client to use for generating notes.
        :param SET_SLIDE_TEXT_FOR_SKIP_SLIDES: Whether to set slide text for 
                                                skip slides.
        :param SET_AI_TEXT_FOR_SKIP_SLIDES: Whether to set AI text for skip
                                            slides.
        :param AI_PROPMT_SKIP_SLIDES: Prompt to use for skip slides.
        :param AI_PROMPT_DCIT_SKIP_SLIDES: Dictionary of prompts to use for
                                            skip slides.
        :param DEFAULT_PROMPT_FOR_OTHER_SLIDES: Prompt to use for other slides.
        :param SKIP_NOTES_FOR_SLIDES_WITH_NOTES: Whether to skip slides with existing notes
        """
        


        

    
