from testapp import app
from flask import render_template
from flask import request
from flask import Flask
from flask import url_for
from flask import session
from flask import redirect
import pandas as pd
import requests
from flask import jsonify
from lxml import etree
import time


app.secret_key = 'tsuruhiro'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'tsuruta':  # パスワードを設定
            session['logged_in'] = True
            return redirect(url_for('sample_form'))
        else:
            return 'ログイン失敗！'
    return render_template('test_app/login.html')

@app.route('/')
def sample_form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('test_app/sample_in.html')

# @app.route('/')
# def sample_form():
#     return render_template('test_app/sample_in.html')
    
@app.route('/sampleform-post', methods=['POST'])
def eSearch():
    IF_filter = request.form.get('IF_filter', 'no')
    url = "https://pubmed.ncbi.nlm.nih.gov/?term="
    URL_1 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json'
    data1 = request.form.get('data1', '')
    data2 = request.form.get('data2', '')
    data3 = request.form.get('data3', '')
    term = '%20'.join([data1, data2, data3])
    retmax = request.form.get('search_limit', '10')
    option = '&retmax='+str(retmax)+'&term='+term
    query = URL_1 + option
    response = requests.get(query)
    response_json = response.json()
    pmid = response_json['esearchresult']['idlist']
    pmid_combine = "+".join(pmid)
    
    if IF_filter == 'no': 
        additional_analysis = request.form.get('additional_analysis', 'no')
        # if additional_analysis == 'no':
        return redirect(url+pmid_combine)
    else:
        list_1000 = 'testapp/data/1000.xlsx'
        df_a_1000 = pd.read_excel(list_1000)
        journal_list_1000 = df_a_1000['Source title'].unique().tolist()
        journal_list_s_1000 = [journal.lower().lstrip('the').replace(' ', '') if journal.lower().startswith('the ') else journal.lower().replace(' ', '') for journal in journal_list_1000]
        list_2000 = 'testapp/data/2000.xlsx'
        df_a_2000 = pd.read_excel(list_2000)
        journal_list_2000 = df_a_2000['Source title'].unique().tolist()
        journal_list_s_2000 = [journal.lower().lstrip('the').replace(' ', '') if journal.lower().startswith('the ') else journal.lower().replace(' ', '') for journal in journal_list_2000]
        esummary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid_combine}&retmode=json"
        URL_2 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&term='
        summary_response = requests.get(esummary_url)
        summary_data = summary_response.json()
        journals = []
        pmids = []
        for uid in summary_data['result']['uids']:
            article = summary_data['result'][uid]
            pmids.append(uid)
            journals.append(article.get('fulljournalname'))
        summary_df = pd.DataFrame({
                "PMID": pmids,
                "Journal": journals
        })
        summary_df['Journal'] = [journal.lower().replace(' ', '').lstrip('the') if journal.lower().startswith('the ') else journal.lower().replace(' ', '') for journal in summary_df['Journal']]
        IF_limit = request.form.get('IF_limit', '8.0')
        if IF_limit == "8.0":     
            filtered_df = summary_df[summary_df['Journal'].isin(journal_list_s_1000)]
            filtered_pmid = filtered_df['PMID']
            filtered_pmid_combine = "+".join(filtered_pmid)
            final_url = url + filtered_pmid_combine   
        else:
            filtered_df = summary_df[summary_df['Journal'].isin(journal_list_s_2000)]
            filtered_pmid = filtered_df['PMID']
            filtered_pmid_combine = "+".join(filtered_pmid)
            final_url = url + filtered_pmid_combine
        return redirect(final_url)
        # IF_limit = request.form.get('IF_limit', '8.0')
        # if IF_limit == "8.0":     
        #     filtered_df = summary_df[summary_df['Journal'].isin(journal_list_s_1000)]
        #     filtered_pmid = filtered_df['pmid']
        #     filtered_pmid_combine = "+".join(filtered_pmid)
        #     final_url = url + filtered_pmid_combine   
        # else:
        #     filtered_df = summary_df[summary_df['Journal'].isin(journal_list_s_2000)]
        #     filtered_pmid = filtered_df['pmid']
        #     filtered_pmid_combine = "+".join(filtered_pmid)
        #     final_url = url + filtered_pmid_combine      
        
            # journal_list = df_summary['Journal'].tolist()
            # journals_str = '\n'.join(journal_list)
            # return journals_str
            # for article in root.findall('.//PubmedArticle'):
            #     pmid = article.find('.//PMID').text
            #     abstract = article.find('.//Abstract/AbstractText')
            #     # pmid_abst = article.find('.//PMID').text
            #     # abstract = article.find('.//AbstractText')
            #     # Abstracts.append(abstract)
            #     # pmids_abst.append(pmid_abst)
            # # df_abst = pd.DataFrame({
            # #     "PMID": pmids_abst,
            # #     "Abstract": Abstracts
            # }) 
            # abst_text =df_abst["Abstract"]
         
        
            # pmid_ab_single = root.find('.//PMID').text
            # abst = root.findall('.//AbstractText')
            # if abst is None:
            #     abst_text = ''
            # else:
            #     abst_text = ''.join(root.xpath('//Abstract//*/text()'))
            #     time.sleep(0.2)
            # responses_abst[pmid_ab_single]=abst_text
            # abst_df = pd.DataFrame.from_dict(responses_abst, orient='index')
            # abst_df.index.name = 'pmid'
            # abst_df.columns = ['Abstract']
            # df_merge = pd.merge(summary_df, abst_df, on='pmid')

            # data4 = request.form.get('data4', '')
            # data5 = request.form.get('data5', '')
            # data6 = request.form.get('data6', '')
            # data7 = request.form.get('data7', '')
            # data8 = request.form.get('data8', '')
            # data9 = request.form.get('data9', '')
            # keywords = [(data4,data5,data6), (data7,data8,data9)]
            # journals = []
            # pmids = []
            # for uid in summary_data['result']['uids']:
            #     article = summary_data['result'][uid]
            #     pmids.append(uid)
            #     journals.append(article.get('fulljournalname'))
            #     df_summary = pd.DataFrame({
            #         "PMID": pmids,
            #         "Journal": journals
            #     })
            
            # journal_list = df_summary['Journal'].tolist()
            # journals_str = '\n'.join(journal_list)
            # return journals_str
            
            
            # queries_abst = [URL_3 + pmid_ab_single for pmid_ab_single in pmid]
            # responses_abst = {}
            # for query_abst in queries_abst:
            #     response_abst = requests.get(query_abst)
            #     root = etree.fromstring(response_abst.content)
            #     pmid_ab_single = root.find('.//PMID').text
            #     abst = root.findall('.//AbstractText')
            #     if abst is None:
            #         abst_text = ''
            #     else:
            #         abst_text = ''.join(root.xpath('//Abstract//*/text()'))
            #         time.sleep(0.2)
            #     responses_abst[pmid_ab_single]=abst_text
            #     abst_df = pd.DataFrame.from_dict(responses_abst, orient='index')
            #     abst_df.index.name = 'pmid'
            #     abst_df.columns = ['Abstract']
            # df_merge = pd.merge(summary_df, abst_df, on='pmid')

            # data4 = request.form.get('data4', '')
            # data5 = request.form.get('data5', '')
            # data6 = request.form.get('data6', '')
            # data7 = request.form.get('data7', '')
            # data8 = request.form.get('data8', '')
            # data9 = request.form.get('data9', '')
            # keywords = [(data4,data5,data6), (data7,data8,data9)]
                
            # def check_keywords_in_same_sentence(abstract, keyword_pairs):
            #     sentences = abstract.split('.')
            #     for sentence in sentences:
            #         if all(any(keyword.lower() in sentence.lower() for keyword in group) for group in keyword_pairs):
            #             return True
            #     return False
            # result = df_merge[df_merge['Abstract'].apply(lambda x: check_keywords_in_same_sentence(x, keywords))]
            # filtered_additional_pmid = result['pmid']
            # filtered_additional_pmid_combine = "+".join(filtered_additional_pmid)
            # final_additional_url = url + filtered_additional_pmid_combine
            # return redirect(final_additional_url)
            
            
            # summary_response = requests.get(esummary_url)
            # summary_data = summary_response.json()
            # journals = []
            # pmids = []
            # for uid in summary_data['result']['uids']:
            #     article = summary_data['result'][uid]
            #     pmids.append(uid)
            #     journals.append(article.get('fulljournalname'))
            #     df_summary = pd.DataFrame({
            #         "PMID": pmids,
            #         "Journal": journals
            #     })
            
            # journal_list = df_summary['Journal'].tolist()
            # journals_str = '\n'.join(journal_list)
            # return journals_str

            # queries = [URL_2 + pmid_single for pmid_single in pmid]
            # summaries = {}
            # for query_single in queries:
            #     summary = requests.get(query_single)
            #     res_title = summary.json()['result']
            #     summaries.update(res_title)
            #     time.sleep(0.2)
            # A_Summaries = [{'pmid':pmid_single, 
            #             'Journal' :summaries[pmid_single]['fulljournalname']} for pmid_single in pmid]
    #         summary_df = pd.DataFrame(A_Summaries)
    #         URL_3 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id='
    #         queries_abst = [URL_3 + pmid_ab_single for pmid_ab_single in pmid]
    #         responses_abst = {}
    #         for query_abst in queries_abst:
    #             response_abst = requests.get(query_abst)
    #             root = etree.fromstring(response_abst.content)
    #             pmid_ab_single = root.find('.//PMID').text
    #             abst = root.findall('.//AbstractText')
    #             if abst is None:
    #                 abst_text = ''
    #             else:
    #                 abst_text = ''.join(root.xpath('//Abstract//*/text()'))
    #                 time.sleep(0.2)
    #             responses_abst[pmid_ab_single]=abst_text
    #             abst_df = pd.DataFrame.from_dict(responses_abst, orient='index')
    #             abst_df.index.name = 'pmid'
    #             abst_df.columns = ['Abstract']
    #         df_merge = pd.merge(summary_df, abst_df, on='pmid')

    #         data4 = request.form.get('data4', '')
    #         data5 = request.form.get('data5', '')
    #         data6 = request.form.get('data6', '')
    #         data7 = request.form.get('data7', '')
    #         data8 = request.form.get('data8', '')
    #         data9 = request.form.get('data9', '')
    #         keywords = [(data4,data5,data6), (data7,data8,data9)]
                
    #         def check_keywords_in_same_sentence(abstract, keyword_pairs):
    #             sentences = abstract.split('.')
    #             for sentence in sentences:
    #                 if all(any(keyword.lower() in sentence.lower() for keyword in group) for group in keyword_pairs):
    #                     return True
    #             return False
    #         result = df_merge[df_merge['Abstract'].apply(lambda x: check_keywords_in_same_sentence(x, keywords))]
    #         filtered_additional_pmid = result['pmid']
    #         filtered_additional_pmid_combine = "+".join(filtered_additional_pmid)
    #         final_additional_url = url + filtered_additional_pmid_combine
    #         return redirect(final_additional_url)
    # else:
    #     list_1000 = 'testapp/data/1000.xlsx'
    #     df_a_1000 = pd.read_excel(list_1000)
    #     journal_list_1000 = df_a_1000['Source title'].unique().tolist()
    #     journal_list_s_1000 = [journal.lower().lstrip('the').replace(' ', '') if journal.lower().startswith('the ') else journal.lower().replace(' ', '') for journal in journal_list_1000]
    #     list_2000 = 'testapp/data/2000.xlsx'
    #     df_a_2000 = pd.read_excel(list_2000)
    #     journal_list_2000 = df_a_2000['Source title'].unique().tolist()
    #     journal_list_s_2000 = [journal.lower().lstrip('the').replace(' ', '') if journal.lower().startswith('the ') else journal.lower().replace(' ', '') for journal in journal_list_2000]
    #     URL_2 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id='
    #     queries = [URL_2 + pmid_single for pmid_single in pmid]
    #     summaries = {}
    #     for query_single in queries:
    #         summary = requests.get(query_single)
    #         res_title = summary.json()['result']
    #         summaries.update(res_title)
    #         time.sleep(0.2)
    #     A_Summaries = [{'pmid':pmid_single, 
    #                 'Journal' :summaries[pmid_single]['fulljournalname']} for pmid_single in pmid]
    #     summary_df = pd.DataFrame(A_Summaries)
    #     summary_df['Journal'] = [journal.lower().replace(' ', '').lstrip('the') if journal.lower().startswith('the ') else journal.lower().replace(' ', '') for journal in summary_df['Journal']]
    #     IF_limit = request.form.get('IF_limit', '8.0')
    #     if IF_limit == "8.0":     
    #         filtered_df = summary_df[summary_df['Journal'].isin(journal_list_s_1000)]
    #         filtered_pmid = filtered_df['pmid']
    #         filtered_pmid_combine = "+".join(filtered_pmid)
    #         final_url = url + filtered_pmid_combine   
    #     else:
    #         filtered_df = summary_df[summary_df['Journal'].isin(journal_list_s_2000)]
    #         filtered_pmid = filtered_df['pmid']
    #         filtered_pmid_combine = "+".join(filtered_pmid)
    #         final_url = url + filtered_pmid_combine  
    #     additional_analysis = request.form.get('additional_analysis', 'no')
    #     if additional_analysis == 'no':
    #         return redirect(final_url)
    #     else:
    #         URL_3 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id='
    #         queries_abst = [URL_3 + pmid_ab_single for pmid_ab_single in filtered_pmid]
    #         responses_abst = {}
    #         for query_abst in queries_abst:
    #             response_abst = requests.get(query_abst)
    #             root = etree.fromstring(response_abst.content)
    #             pmid_ab_single = root.find('.//PMID').text
    #             abst = root.findall('.//AbstractText')
    #             if abst is None:
    #                 abst_text = ''
    #             else:
    #                 abst_text = ''.join(root.xpath('//Abstract//*/text()'))
    #                 time.sleep(0.2)
    #             responses_abst[pmid_ab_single]=abst_text
    #             abst_df = pd.DataFrame.from_dict(responses_abst, orient='index')
    #             abst_df.index.name = 'pmid'
    #             abst_df.columns = ['Abstract']
    #         df_merge = pd.merge(filtered_df, abst_df, on='pmid')

    #         data4 = request.form.get('data4', '')
    #         data5 = request.form.get('data5', '')
    #         data6 = request.form.get('data6', '')
    #         data7 = request.form.get('data7', '')
    #         data8 = request.form.get('data8', '')
    #         data9 = request.form.get('data9', '')
    #         keywords = [(data4,data5,data6), (data7,data8,data9)]
            
    #         def check_keywords_in_same_sentence(abstract, keyword_pairs):
    #             sentences = abstract.split('.')
    #             for sentence in sentences:
    #                 if all(any(keyword.lower() in sentence.lower() for keyword in group) for group in keyword_pairs):
    #                     return True
    #             return False
    #         result = df_merge[df_merge['Abstract'].apply(lambda x: check_keywords_in_same_sentence(x, keywords))]
    #         filtered_additional_pmid = result['pmid']
    #         filtered_additional_pmid_combine = "+".join(filtered_additional_pmid)
    #         final_additional_url = url + filtered_additional_pmid_combine
    #         return redirect(final_additional_url)