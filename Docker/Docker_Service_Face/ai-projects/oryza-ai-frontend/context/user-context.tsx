import { userApi } from "@/api-client/setting";
import { authApi } from "@/api-client";
import { UserRes } from "@/interfaces/user";
import { useDebouncedValue } from "@mantine/hooks";

import {
    Dispatch,
    SetStateAction,
    createContext,
    useContext,
    useEffect,
    useMemo,
    useState,
    useCallback,
  } from "react";

export type UserContextType = {
    data: UserRes[];
    setData: Dispatch<SetStateAction<UserRes[]>>;
    total: number;
    setTotal: Dispatch<SetStateAction<number>>;
    isAdmin: boolean;
    setIsAdmin: Dispatch<SetStateAction<boolean>>;
    isSuperUser: boolean;
    setIsSuperUser: Dispatch<SetStateAction<boolean>>;
    textSearch: string;
    setTextSearch: Dispatch<SetStateAction<string>>;
};

export const UserContext = createContext({} as UserContextType);

type TProps = {
    children: React.ReactNode;
};

export const UserProvider = ({ children }: TProps) => {
    const [data, setData] = useState<UserRes[]>([]);
    const [total, setTotal] = useState(0);
    const [textSearch, setTextSearch] = useState("");
    const [debounced] = useDebouncedValue(textSearch, 500);
    const [isAdmin, setIsAdmin] = useState(false); 
    const [isSuperUser, setIsSuperUser] = useState(false); 
    const getCount = useCallback(async () => {
        await userApi
            .getCount({ data_search: textSearch })
            .then((res: any) => {
                setTotal(Number(res.data?.count ?? 0));
            })
            .catch((e) => {
                console.log("get count user Error: ", e);
            });
    }, [debounced]);

    useEffect(() => {
        getCount();
    }, [getCount()]);

    const getMe = async () => {
        await authApi
            .getProfile()
            .then((res: any) => {
                setIsSuperUser(res.data?.is_superuser ?? false);
                setIsAdmin(res.data?.is_admin ?? false);
            })
            .catch((e) => {
                console.log("get me Error: ", e);
            });
    }

    useEffect(() => {
        getMe();
    }, []);

    const value = useMemo(
        () => ({
            data,
            setData,
            total,
            setTotal,
            isAdmin,
            setIsAdmin,
            isSuperUser,
            setIsSuperUser,
            textSearch,
            setTextSearch,
        }),
        [
            data, setData, 
            setTotal, total, 
            isAdmin, setIsAdmin, 
            isSuperUser, setIsSuperUser, 
            textSearch, setTextSearch
        ]
    );

    return (
        <UserContext.Provider value={value}>{children}</UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);