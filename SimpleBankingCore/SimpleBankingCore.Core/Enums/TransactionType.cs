namespace SimpleBankingCore.Core.Enums
{
    public enum TransactionType
    {
        Deposit,
        Withdrawal,
        TransferOut, // When money leaves this account during a transfer
        TransferIn   // When money enters this account during a transfer
    }
}
