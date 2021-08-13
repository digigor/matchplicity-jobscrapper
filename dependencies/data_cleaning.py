# -*- coding: utf-8 -*-

import unicodedata2
import unicodedata
import re


#TODO falta testear
class DataCleaner:
    '''
        This class allow us to sanitaze the information we need to extract.
    '''

    def remove_control_characters(self, string):
        '''
        This method removes all control characters from unicode text.
        :param string: The string you want the control characters removed from
        :return: string
        '''
        return "".join(character for character in string if unicodedata.category(character)[0] != "C")

    def RemoveAccents(self, input_str):
        '''
            This methods allow is to remove the accents from a input string
        :param input_str: string to be changed
        :return: string with the accents removed
        '''
        nfkd_form = unicodedata2.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata2.combining(c)])

    def MatcherParser(self, texto):
        '''
            This method allow us to receive a string and do some operations to it,
            like lower cases, remove blank spaces from the begining to the end of the string,
            and replace some typos characters.
        :param texto: string to be changed
        :return: string changed
        '''

        texto = texto.lower()
        texto = texto.lstrip(' ').rstrip(' ')
        texto = texto.replace(" ", "").replace("-", "").replace("/", "").replace("\n", "")

        texto = self.RemoveAccents(texto)

        return (texto)

    def StringConverterToSave(self, texto):
        '''
            This method receive a string text and normalize it. Doesn't replace the space blank
        :param texto: string to be normalized
        :return: texto: string normalized
        '''

        if type(texto) ==  list:
            lista = []
            for i in texto:
                i = i.lower()
                i = i.lstrip(' ').rstrip(' ')
                #i = i.replace("-", "").replace("/", "").replace("\n", "").replace("(", "").replace(")", "")

                i = self.RemoveAccents(i)
                lista.append(i)
            return lista
        else:
            texto = texto.lower()
            texto = texto.lstrip(' ').rstrip(' ')
            texto = texto.replace("-", "").replace("/", "").replace("\n", "")

            texto = self.RemoveAccents(texto)
            # Para imprimir HTML Limpio
            #print(texto)
            return (texto)


    def StringConverterToMatch(self, texto):
        '''
           This method receive a string text and normalize it.
        :param texto: string to be normalized
        :return: texto: string normalized
        '''

        texto = texto.lower()
        texto = texto.lstrip(' ').rstrip(' ')
        texto = texto.replace(" ", "").replace("-", "").replace("/", "").replace("\n", "")

        texto = self.RemoveAccents(texto)

        return (texto)

    def NumberCleaner(self,NumberToClean):
        '''
            This method receive a string text and cleaned it to Deciaml number format.
            :param NumberToClean: string to be cleaned, only whit 2 or 1 decimal numbers
            :return: NumberCleaned: Decimal number
        '''
        try:
            Patron= r'[0-9].*'
            PatronCompilado=re.compile(Patron,re.DOTALL)
            NumberCleaned=re.findall(PatronCompilado,NumberToClean) # Cleaning first non numeric caracters
            if NumberCleaned:
                NumberCleaned=str(NumberCleaned).replace(',','.').replace('o','0').replace(' ','') #Replace all ',' for '.' and replace 'o' for '0', and remove white spaces
                Patron = r'([0-9.]+)'
                PatronCompilado = re.compile(Patron, re.DOTALL)
                NumberCleaned=re.findall(PatronCompilado,NumberCleaned) #Find all completed numbers whit dots and group in a list of elements
                if NumberCleaned:
                    NumberCleaned=NumberCleaned[0] #take only the first element of the list (other elements considered as trash data)
                    Patron = r'\.(?!\w)'
                    PatronCompilado = re.compile(Patron, re.DOTALL)
                    NumberCleaned=re.sub(PatronCompilado,'',NumberCleaned) #Remove extra dots and final dots
                    Patron = r'[^0-9.]|\.(?=.*\.)'
                    PatronCompilado = re.compile(Patron, re.DOTALL)
                    NumberCleaned=re.sub(PatronCompilado,'',NumberCleaned) #Remove all dots except posible final decimal dots
                    Patron = r'\.(?=[0-9]{3,})'
                    PatronCompilado = re.compile(Patron, re.DOTALL)
                    NumberCleaned=re.sub(PatronCompilado,'',NumberCleaned) #Finaly remove the remain dot if not a decimal dot
                return (NumberCleaned)
            else:
                return (None)
        except Exception as e:
            print(e)
            return ('000000000') #Error in the process of datacleaner
            Raise

    def RemoveExtraWhiteSpce(self,InputString):
        '''
                    This methods allow us to remove extra space between words in strings and trim left an right finals spaces.
                :param inputstr: string to be changed
                :return: string whit extra space removed
                '''
        try:
            Resultado= re.sub(r'\s{2,}',' ',InputString)
            return str(Resultado).lstrip(' ').rstrip(' ')
        except Exception as e:
            print(e)
            return (InputString)
            raise

    def RemoveSemiColon(self, InputString):
        '''
                    This methods allow us to remove semicolons in strings and trim left an right finals spaces.
                :param inputstr: string to be changed
                :return: string whit extra space removed
                '''
        try:
            Resultado= re.sub(r';', '.', InputString)
            return str(Resultado)
        except Exception as e:
            print(e)
            return (InputString)
            raise

    def RmvWhiteSpceBtwnNumbers(self,InputString):
        '''
            This methods allow us to remove white space between numbers in strings.
            :param inputstr: string to be changed
            :return: string whit extra space removed
        '''
        try:
            Resultado= re.sub(r'(?<=\d)\s+(?=\d)','',InputString)
            return  (Resultado)
        except Exception as e:
            print(e)
            return (InputString)
            raise

    def RmvLineBreak(self, InputString):
        '''
            This methods allow us to remove white space between numbers in strings.
            :param inputstr: string to be changed
            :return: string whit extra space removed
        '''
        try:
            Resultado = re.sub(r'\n', ' ', InputString)
            Resultado = re.sub(r'\r', ' ', InputString)
            return (Resultado)
        except Exception as e:
            print(e)
            return (InputString)
            raise

    def DNIExtractor(self, InputString):
        '''
            This methods allow us to extract the DNI field from a string... only acept one DNI for string
            :param inputstr: string to be changed
            :return: tuple of ['CleanString','DNI Number']
        '''
        try:
            #first we need to clear the spaces between numbers, "-" and extrawhite spaces.
            InputString=re.sub(r'[-]',' ',InputString)
            InputString=self.RemoveExtraWhiteSpce(InputString)
            InputString=self.RmvWhiteSpceBtwnNumbers(InputString)
            # Now we extract the DNI field
            DNIField= re.findall(r'(ficha:*|folio|\(?\s?pasaporte:?\s?\D{0,3}|\s?pasaporte pas\.?\s?|\(?cedula\s?\D*|ced\.? n|ced\.* e|ced\.*|\(?ruc:?|\sn|\se)*(\s*?|\.*?|,*?)(?:\()*?([0-9]{5,})(?:\))?',InputString,re.IGNORECASE)
            if DNIField:
                #Cat result, remove DNI from name and return List
                DNIField = ''.join(DNIField[0])
                CleanName =re.sub(r'(ficha:*|folio|\(?\s?pasaporte:?\s?\D{0,3}|\s?pasaporte pas\.?\s?|\(?cedula\s?\D*?|ced\.? n|ced\.* e|ced\.*|\(?ruc:?|\sn|\se)*(\s*?|\.*?|,*?)\(*?[0-9]{5,}(\))?','',InputString)
                return [str(CleanName).rstrip().lstrip(), str(DNIField).rstrip().lstrip()]
            else:
                #Not DNI Detected, return list without DNI
                CleanName=InputString
                return [str(CleanName).rstrip().lstrip(),'']
        except Exception as e:
            print("::DataCleaner:: Error in Extract DNI Method {}".format(e) )
            return [InputString,'']

