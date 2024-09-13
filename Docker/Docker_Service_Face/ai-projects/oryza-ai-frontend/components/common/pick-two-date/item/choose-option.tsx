import CheckRoundedIcon from '@mui/icons-material/CheckRounded';
import { ListItemIcon, MenuList, Stack, Typography } from '@mui/material';
import 'dayjs/locale/vi';
import { TimeOption, renderTimeOption, timeOption } from '../function';
import Scrollbar from '../../scrollbar';
import { useRef } from 'react';
import { useDraggable } from 'react-use-draggable-scroll';

export interface IChooseTimeOptionProps {
    option: TimeOption | null;
    setoption: any;
    getBeforeDay: (daysToSubtract: number | 'ALL') => void;
}

export function ChooseTimeOption(props: IChooseTimeOptionProps) {
    const { option, setoption, getBeforeDay } = props;
    const ref = useRef<HTMLDivElement>() as React.MutableRefObject<HTMLInputElement>;
    const { events } = useDraggable(ref, {
        applyRubberBandEffect: true,
    });
    return (
        <Stack
            sx={{
                my: { xs: '10px', sm: '20px' },
                pl: '20px',
                borderLeft: '1px solid #ECF4FF',
                alignItems: 'flex-start',
                mt: { xs: 0, sm: '20px' },
                borderBottom: { xs: '1px solid #ECF4FF', sm: 'none' },
            }}
        >
            <Stack>
                <Typography
                    sx={{
                        color: '#808080',
                        fontSize: { xs: '14px', sm: '16px' },
                        fontWeight: 400,
                        padding: 0,
                        userSelect: 'none',
                        marginBottom: '20px',
                        display: { xs: 'none', md: 'flex' },
                    }}
                >
                    Ngày được xác định
                </Typography>

                <Stack
                    sx={{ width: { xs: '90vw', sm: '170px' }, height: { xs: '50px', sm: 'auto' } }}
                >
                    <Stack
                        {...events}
                        ref={ref}
                        sx={{
                            overflow: 'auto',
                            '&::-webkit-scrollbar': {
                                width: '2px',
                                height: '2px',
                            },
                            '&::-webkit-scrollbar-thumb': {
                                backgroundColor: 'transparent',
                                borderRadius: '4px',
                            },
                            py: 1,
                        }}
                        direction={{ xs: 'row', sm: 'column' }}
                        spacing={{ xs: 5, sm: 1 }}
                    >
                        {timeOption.map((value: TimeOption) => {
                            let isActive = value == option;

                            return (
                                <Stack
                                    key={value}
                                    onClick={() => {
                                        setoption(value);
                                        switch (value) {
                                            case 'ALL':
                                                getBeforeDay('ALL');
                                                break;
                                            case 'YESTERDAY':
                                                getBeforeDay(1);
                                                break;
                                            case '7-DAY-AGO':
                                                getBeforeDay(7);
                                                break;
                                            case '30-DAY-AGO':
                                                getBeforeDay(30);
                                                break;
                                            case '90-DAY-AGO':
                                                getBeforeDay(90);
                                                break;
                                            case '180-DAY-AGO':
                                                getBeforeDay(180);
                                                break;
                                            case '365-DAY-AGO':
                                                getBeforeDay(365);
                                                break;
                                            default:
                                                break;
                                        }
                                    }}
                                    sx={{
                                        display: 'flex',
                                        flexDirection: 'row',
                                        gap: '8px',
                                        alignItems: 'center',
                                        cursor: 'pointer',
                                        padding: ' 4px 0',
                                        marginTop: '3px',
                                        marginBottom: '3px',
                                    }}
                                >
                                    <Typography
                                        sx={{
                                            color: isActive ? '#007dc0' : '#808080',
                                            fontSize: { xs: '16px', sm: '14x' },
                                            fontStyle: 'normal',
                                            fontWeight: { xs: 500, sm: 400 },
                                            lineHeight: '140%',
                                            cursor: 'pointer',
                                            userSelect: 'none',
                                            transition: ' all 0.3s ease-in-out',
                                            whiteSpace: 'nowrap',
                                        }}
                                    >
                                        {renderTimeOption(value)}
                                    </Typography>
                                    {isActive && (
                                        <CheckRoundedIcon sx={{ color: '#007dc0', fontSize: 17 }} />
                                    )}
                                </Stack>
                            );
                        })}
                    </Stack>
                </Stack>
            </Stack>
        </Stack>
    );
}
