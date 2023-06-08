import { Pivot, PivotItem } from "@fluentui/react";
import DOMPurify from "dompurify";

import styles from "./AnalysisPanel.module.css";

import { SupportingContent } from "../SupportingContent";
import { AnalysisPanelTabs } from "./AnalysisPanelTabs";

// interface Props {
//     className: string;
//     activeTab: AnalysisPanelTabs;
//     onActiveTabChanged: (tab: AnalysisPanelTabs) => void;
//     activeCitation: string | undefined;
//     citationHeight: string;
//     answer: AskResponse;
// }



const pivotItemDisabledStyle = { disabled: true, style: { color: "grey" } };

export const AnalysisPanel = ({ answer, activeTab, activeCitation, citationHeight, className, onActiveTabChanged }) => {
    const isDisabledThoughtProcessTab = !answer.thoughts;
    const isDisabledSupportingContentTab = !answer.data_points.length;
    const isDisabledCitationTab = !activeCitation;

    const sanitizedThoughts = DOMPurify.sanitize(answer.thoughts);
    const getCitationFilePath = (citation) => {
        const directories = citation.split('/')
        let stage2Found = false
        let filepath = ""
        for(const dir of directories){
            if(dir.includes('-stage2')){
                stage2Found = true
            }
            if(stage2Found){
                filepath += dir + '/'
            }
        }
        let count = 0
        let newFilePath = ""
        for(const chunk of filepath.split('_')){
            if(count++ > 1){
                newFilePath += chunk 
                if(count < filepath.split('_').length){
                    newFilePath += '_'
                }
            }
        }
        newFilePath = newFilePath.replace('.txt/','')
        return newFilePath
    }
    

    return (
        <Pivot
            className={className}
            selectedKey={activeTab}
            onLinkClick={pivotItem => pivotItem && onActiveTabChanged(pivotItem.props.itemKey)}
        >
            <PivotItem
                itemKey={AnalysisPanelTabs.ThoughtProcessTab}
                headerText="Thought process"
                headerButtonProps={isDisabledThoughtProcessTab ? pivotItemDisabledStyle : undefined}
            >
                <div className={styles.thoughtProcess} dangerouslySetInnerHTML={{ __html: sanitizedThoughts }}></div>
            </PivotItem>
            <PivotItem
                itemKey={AnalysisPanelTabs.SupportingContentTab}
                headerText="Supporting content"
                headerButtonProps={isDisabledSupportingContentTab ? pivotItemDisabledStyle : undefined}
            >
                <SupportingContent supportingContent={answer.data_points} />
            </PivotItem>
            <PivotItem
                itemKey={AnalysisPanelTabs.CitationTab}
                headerText="Citation"
                headerButtonProps={isDisabledCitationTab ? pivotItemDisabledStyle : undefined}
            >
                <iframe title="Citation" src={`/api/viewpdf?container=documents&filename=${getCitationFilePath(activeCitation)}`} width="100%" height={citationHeight} />
            </PivotItem>
        </Pivot>
    );
};
