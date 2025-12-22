export type IExpectations = {
    text: string;
    icon: string;
};

export type IComingSoon = {
    icon: string;
    alert: string;
    intro: string;
    expectations: IExpectations[];
};
