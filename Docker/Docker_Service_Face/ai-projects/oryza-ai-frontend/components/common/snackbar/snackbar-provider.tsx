import { SnackbarProvider, closeSnackbar } from 'notistack';
import * as React from 'react';
import { ReportComp } from './report';

export interface ISnackbarProviderCustomProps {
    children?: React.ReactNode | undefined;
}

export default function SnackbarProviderCustom(props: ISnackbarProviderCustomProps) {
    return (
        <SnackbarProvider
            Components={{
                success: ReportComp,
                default: ReportComp,
                error: ReportComp,
                info: ReportComp,
                warning: ReportComp,
            }}
            maxSnack={3}
        >
            {props.children}
        </SnackbarProvider>
    );
}
