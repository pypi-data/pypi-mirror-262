import { IChart } from "@kanaries/graphic-walker/dist/interfaces";
export declare function usePythonCode(props: {
    sourceCode: string;
    visSpec: IChart[];
    version: string;
}): {
    pyCode: string;
};
