#nullable enable
using Microsoft.EntityFrameworkCore;
using SimpleBankingCore.Data.Context;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Linq.Expressions;

namespace SimpleBankingCore.Data.Repositories
{
    // Generic implementation of the IRepository interface
    public class GenericRepository<T> : IRepository<T> where T : class
    {
        protected readonly BankingDbContext _context;
        protected readonly DbSet<T> _dbSet;

        public GenericRepository(BankingDbContext context)
        {
            _context = context;
            _dbSet = _context.Set<T>();
        }

        public async Task<T?> GetByIdAsync(int id)
        {
            return await _dbSet.FindAsync(id);
        }

        public async Task<IEnumerable<T>> GetAllAsync()
        {
            return await _dbSet.ToListAsync();
        }

        public async Task AddAsync(T entity)
        {
            await _dbSet.AddAsync(entity);
        }

        public Task UpdateAsync(T entity)
        {
            _dbSet.Update(entity);
            return Task.CompletedTask;
        }

        public async Task DeleteAsync(int id)
        {
            var entity = await _dbSet.FindAsync(id);
            if (entity != null)
            {
                _dbSet.Remove(entity);
            }
        }

        public async Task<int> SaveChangesAsync()
        {
            return await _context.SaveChangesAsync();
        }

        public async Task<T?> GetSingleOrDefaultAsync(Expression<System.Func<T, bool>> predicate, params Expression<System.Func<T, object>>[] includes)
        {
            IQueryable<T> query = _dbSet;
            foreach (var include in includes)
            {
                query = query.Include(include);
            }
            return await query.SingleOrDefaultAsync(predicate);
        }

        public async Task<IEnumerable<T>> FindAsync(Expression<System.Func<T, bool>> predicate)
        {
            return await _dbSet.Where(predicate).ToListAsync();
        }
    }
}
